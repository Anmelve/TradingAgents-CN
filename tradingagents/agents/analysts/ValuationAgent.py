import os
import json
import re
import ast
from tradingagents.utils.logging_init import get_logger
from langchain_core.prompts import ChatPromptTemplate

logger = get_logger("analysts.valuation")


def create_valuation_analyst(llm, toolkit):
    """
    Create a DCF Valuation Analyst node for the analyst team.
    """

    def valuation_analyst_node(state):
        ticker = state.get("company_of_interest")
        region = state.get("market_type", "US").lower()
        current_date = state.get("trade_date")

        # Fetch API keys from environment/config
        finnhub_api_key = os.getenv("FINNHUB_API_KEY")
        tushare_api_key = os.getenv("TUSHARE_TOKEN")
        logger.debug(f"FINNHUB_API_KEY loaded: {'SET' if finnhub_api_key else 'NOT SET'} ({str(finnhub_api_key)[:6]}...)")
        logger.debug(f"TUSHARE_TOKEN loaded: {'SET' if tushare_api_key else 'NOT SET'} ({str(tushare_api_key)[:6]}...)")

        # --- Fetch FCF and revenue ---
        fcf, revenue, shares_outstanding = 0, 0, 0
        if region not in ("us", "us stocks", "us stock"):
            logger.error(f"Unsupported region: {region}. ValuationAgent only supports US stocks.")
            return {"error": "ValuationAgent only supports US stocks."}

        try:
            import yfinance as yf

            stock = yf.Ticker(ticker)
            cashflow = stock.cashflow
            financials = stock.financials
            stock_info = stock.info

            if 'Free Cash Flow' in cashflow.index:
                fcf = cashflow.loc['Free Cash Flow'].iloc[0]
                logger.info(f"Free Cash Flow found directly: {fcf}")
            else:
                logger.info("Free Cash Flow not found, calculating from Operating Cash Flow and Capex.")
                if 'Operating Cash Flow' in cashflow.index:
                    operating_cf = cashflow.loc['Operating Cash Flow'].iloc[0]
                elif 'Total Cash From Operating Activities' in cashflow.index:
                    operating_cf = cashflow.loc['Total Cash From Operating Activities'].iloc[0]
                else:
                    logger.error(f"Missing Operating Cash Flow field in Yahoo Finance cashflow: {cashflow.index.tolist()}")
                    return {"valuation_report": f"Error: Missing Operating Cash Flow field in Yahoo Finance cashflow: {cashflow.index.tolist()}"}

                if 'Capital Expenditure' in cashflow.index:
                    capex = cashflow.loc['Capital Expenditure'].iloc[0]
                elif 'Capital Expenditures' in cashflow.index:
                    capex = cashflow.loc['Capital Expenditures'].iloc[0]
                else:
                    logger.error(f"Missing Capital Expenditure field in Yahoo Finance cashflow: {cashflow.index.tolist()}")
                    return {"valuation_report": f"Error: Missing Capital Expenditure field in Yahoo Finance cashflow: {cashflow.index.tolist()}"}

                fcf = operating_cf + capex
                logger.info(f"Calculated Free Cash Flow: {fcf} (Operating CF: {operating_cf}, Capex: {capex})")

            if 'Total Revenue' in financials.index:
                revenue = financials.loc['Total Revenue'].iloc[0]
            else:
                logger.error(f"Missing Revenue field in Yahoo Finance financials: {financials.index.tolist()}")
                return {"valuation_report": f"Error: Missing Revenue field in Yahoo Finance financials: {financials.index.tolist()}"}

            if 'sharesOutstanding' in stock_info:
                shares_outstanding = stock_info['sharesOutstanding']
                logger.info(f"Shares Outstanding: {shares_outstanding}")
            else:
                logger.warning("Shares outstanding not found in stock info, using market cap / current price as fallback")
                current_price = stock_info.get('currentPrice', 0)
                market_cap = stock_info.get('marketCap', 0)
                if current_price > 0 and market_cap > 0:
                    shares_outstanding = market_cap / current_price
                    logger.info(f"Calculated Shares Outstanding: {shares_outstanding} (Market Cap: {market_cap}, Current Price: {current_price})")
                else:
                    logger.error("Could not determine shares outstanding")
                    shares_outstanding = 0

        except Exception as e:
            logger.error(f"Failed to fetch FCF/Revenue from Yahoo Finance: {e}")
            return {"valuation_report": f"Error: Could not fetch FCF/Revenue from Yahoo Finance. {e}"}

        if fcf == 0:
            logger.error(f"Could not fetch FCF data for ticker {ticker} in region {region}")
            return {"error": "Could not fetch FCF data"}

        # --- Use LLM to get valuation parameters ---
        system_message = (
            "You are a professional DCF valuation expert. "
            "You must estimate a reasonable FCF growth rate, discount rate, and terminal growth rate for the following company and explain your reasoning in detail. "
            "Return your answer WITH JSON ONLY and in the following STRICT JSON format (all property names and string values must use double quotes): "
            '{ "growth_rate": <float>, "discount_rate": <float>, "terminal_growth_rate": <float>, "reasoning": <string> }'
        )

        user_message = (
            f"Company: {ticker}\n"
            f"Region: {region}\n"
            f"Revenue: {revenue}\n"
            f"Free Cash Flow: {fcf}\n"
            f"Years: 5\n"
            f"Please estimate a reasonable FCF growth rate, discount rate, and terminal growth rate for this company."
        )

        logger.info(f"Prompt sent to LLM (system): {system_message}")
        logger.info(f"Prompt sent to LLM (user): {user_message}")

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_message),
                ("human", user_message)
            ])
            chain = prompt | llm
            response = chain.invoke({"user_message": user_message})

            logger.error(f"Raw LLM response: {response}")
            logger.debug(f"Raw LLM response type: {type(response)}")
            logger.debug(f"Raw LLM response: {getattr(response, 'content', response)}")

            response_text = getattr(response, "content", str(response))

            # Remove markdown code block wrappers if present
            response_text = response_text.strip()
            if response_text.startswith("```json") or response_text.startswith("```"):
                response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
                response_text = re.sub(r"\s*```$", "", response_text)

            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                json_text = match.group()
                try:
                    parsed = json.loads(json_text)
                except Exception as e_json:
                    logger.error(f"json.loads failed: {e_json}, try ast.literal_eval")
                    parsed = ast.literal_eval(json_text)

                growth_rate = parse_rate(parsed.get("growth_rate", 0.08), 0.08)
                discount_rate = parse_rate(parsed.get("discount_rate", 0.1), 0.1)
                terminal_growth_rate = parse_rate(parsed.get("terminal_growth_rate", 0.03), 0.03)
                reasoning = parsed.get("reasoning", response_text)
            else:
                raise ValueError("No JSON found in LLM response")

        except Exception as e:
            logger.error(f"LLM growth rate/discount/terminal extraction failed: {e}")
            match = re.search(r"([0-9.]+)\s*%", response_text)
            growth_rate = float(match.group(1)) / 100.0 if match else 0.08
            discount_rate = 0.1
            terminal_growth_rate = 0.03
            reasoning = f"Defaulted to 8% growth rate, 10% discount rate, 3% terminal growth rate due to LLM error: {e}"

        # --- DCF Calculation ---
        N = 5
        fcf_list = [fcf * ((1 + growth_rate) ** i) for i in range(1, N + 1)]
        discounted_fcf = [fcf_list[i] / ((1 + discount_rate) ** (i + 1 - 1)) for i in range(N)]
        terminal_value = (fcf_list[-1] * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
        discounted_terminal = terminal_value / ((1 + discount_rate) ** N)
        dcf_value = sum(discounted_fcf) + discounted_terminal

        per_share_dcf_value = dcf_value / shares_outstanding if shares_outstanding > 0 else 0

        valuation_report_str = (
            f"DCF Value: {dcf_value if dcf_value is not None else 'N/A'}\n"
            f"Per-Share DCF Value: ${per_share_dcf_value:.2f}\n"
            f"Growth Rate: {growth_rate * 100:.2f}%\n"
            f"Discount Rate: {discount_rate * 100:.2f}%\n"
            f"Terminal Growth Rate: {terminal_growth_rate * 100:.2f}%\n"
            f"Reasoning: {reasoning}"
        )

        output_dict = {
            "valuation_report": valuation_report_str,
            "dcf_value": dcf_value,
            "growth_rate": growth_rate,
            "discount_rate": discount_rate,
            "terminal_growth_rate": terminal_growth_rate,
            "reasoning": reasoning,
            "fcf": fcf,
            "revenue": revenue,
            "ticker": ticker,
            "region": region,
            "stock_price": state.get("stock_price"),
            "shares_outstanding": shares_outstanding,
            "per_share_dcf_value": per_share_dcf_value,
        }

        logger.debug(f"ValuationAgent output: {output_dict}")
        return output_dict

    return valuation_analyst_node


def parse_rate(val, default):
    try:
        val = float(val)
        return val / 100.0 if val > 1 else val
    except Exception:
        return default
