import os
from tradingagents.utils.logging_init import get_logger
logger = get_logger("analysts.valuation")
from langchain_core.prompts import ChatPromptTemplate

# The LLM instance will be passed in, as with other analysts

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
        # Debug log for API keys (mask for security)
        logger.debug(f"FINNHUB_API_KEY loaded: {'SET' if finnhub_api_key else 'NOT SET'} ({str(finnhub_api_key)[:6]}...)")
        logger.debug(f"TUSHARE_TOKEN loaded: {'SET' if tushare_api_key else 'NOT SET'} ({str(tushare_api_key)[:6]}...)")

        # --- Fetch FCF and revenue ---
        fcf, revenue = 0, 0
        if region in ("us", "us stocks", "us stock"):
            try:
                import yfinance as yf
                stock = yf.Ticker(ticker)
                cashflow = stock.cashflow
                financials = stock.financials

                # Try to get Free Cash Flow directly
                if 'Free Cash Flow' in cashflow.index:
                    fcf = cashflow.loc['Free Cash Flow'].iloc[0]
                    logger.info(f"Free Cash Flow found directly: {fcf}")
                else:
                    # Fallback: Try to get Operating Cash Flow
                    logger.info("Free Cash Flow not found, calculating from Operating Cash Flow and Capex.")
                    if 'Operating Cash Flow' in cashflow.index:
                        operating_cf = cashflow.loc['Operating Cash Flow'].iloc[0]
                    elif 'Total Cash From Operating Activities' in cashflow.index:
                        operating_cf = cashflow.loc['Total Cash From Operating Activities'].iloc[0]
                    else:
                        logger.error(f"Missing Operating Cash Flow field in Yahoo Finance cashflow: {cashflow.index.tolist()}")
                        return {"valuation_report": f"Error: Missing Operating Cash Flow field in Yahoo Finance cashflow: {cashflow.index.tolist()}"}

                    # Try to get Capital Expenditure
                    if 'Capital Expenditure' in cashflow.index:
                        capex = cashflow.loc['Capital Expenditure'].iloc[0]
                    elif 'Capital Expenditures' in cashflow.index:
                        capex = cashflow.loc['Capital Expenditures'].iloc[0]
                    else:
                        logger.error(f"Missing Capital Expenditure field in Yahoo Finance cashflow: {cashflow.index.tolist()}")
                        return {"valuation_report": f"Error: Missing Capital Expenditure field in Yahoo Finance cashflow: {cashflow.index.tolist()}"}

                    fcf = operating_cf + capex
                    logger.info(f"Calculated Free Cash Flow: {fcf} (Operating CF: {operating_cf}, Capex: {capex})")

                # Revenue
                if 'Total Revenue' in financials.index:
                    revenue = financials.loc['Total Revenue'].iloc[0]
                else:
                    logger.error(f"Missing Revenue field in Yahoo Finance financials: {financials.index.tolist()}")
                    return {"valuation_report": f"Error: Missing Revenue field in Yahoo Finance financials: {financials.index.tolist()}"}

            except Exception as e:
                logger.error(f"Failed to fetch FCF/Revenue from Yahoo Finance: {e}")
                return {"valuation_report": f"Error: Could not fetch FCF/Revenue from Yahoo Finance. {e}"}
        elif region in ("cn", "a-shares", "a股"):
            try:
                import tushare as ts
                ts.set_token(tushare_api_key)
                pro = ts.pro_api()
                df = pro.cashflow(ts_code=ticker, fields="n_cashflow_act")
                fcf = float(df.iloc[0]["n_cashflow_act"])
                df2 = pro.income(ts_code=ticker, fields="revenue")
                revenue = float(df2.iloc[0]["revenue"])
            except Exception as e:
                logger.error(f"Failed to fetch CN FCF: {e}")
        else:
            logger.error(f"Unsupported region: {region}")
            return {"error": "Unsupported region"}

        if fcf == 0:
            logger.error(f"Could not fetch FCF data for ticker {ticker} in region {region}")
            return {"error": "Could not fetch FCF data"}

        # --- Use LLM to get growth rate, DCF value, and reasoning ---
        system_message = (
            "You are a professional DCF valuation expert. "
            "You must estimate a reasonable FCF growth rate for the following company and explain your reasoning in detail. "
            "Then, using the following DCF formula, calculate the DCF value for the company. "
            "DCF Formula: DCF = sum_{{i=1}}^N [FCF_i / (1 + r)^i] + [FCF_N * (1 + g) / (r - g)] / (1 + r)^N. "
            "Where FCF_i is the projected free cash flow for year i, r is the discount rate, g is the terminal growth rate, and N is the number of years (here N=5). "
            "Use the provided FCF, growth rate, discount rate, and terminal growth rate. "
            "Return the predicted growth rate (as a percentage), the DCF value, and your detailed reasoning. "
            "Do not fabricate data. Use only the information provided. "
            "Return your answer WITH JSON ONLY and in the following STRICT JSON format (all property names and string values must use double quotes): {{ \"growth_rate\": <float>, \"dcf_value\": <float>, \"reasoning\": <string> }}"
        )

        user_message = (
            f"Company: {ticker}\n"
            f"Region: {region}\n"
            f"Revenue: {revenue}\n"
            f"Free Cash Flow: {fcf}\n"
            f"Discount Rate: 0.1\n"
            f"Terminal Growth Rate: 0.03\n"
            f"Years: 5\n"
            f"Please estimate a reasonable FCF growth rate, then use the DCF formula to calculate the DCF value, and explain your reasoning."
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
            if hasattr(response, "content"):
                response_text = response.content
            else:
                response_text = str(response)
            import json
            import re
            import ast
            # Try to parse JSON from the response
            try:
                match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if match:
                    json_text = match.group()
                    try:
                        parsed = json.loads(json_text)
                    except Exception as e_json:
                        logger.error(f"json.loads failed: {e_json}, try ast.literal_eval")
                        parsed = ast.literal_eval(json_text)
                    growth_rate = float(parsed.get("growth_rate", 0.08))
                    dcf_value = float(parsed.get("dcf_value", 0.0))
                    reasoning = parsed.get("reasoning", response_text)
                    logger.info(f"growth_rate: {growth_rate}")
                else:
                    raise ValueError("No JSON found in LLM response")
            except Exception as e:
                logger.error(f"Failed to parse LLM JSON response: {e}")
                logger.error(f"LLM原始返回内容: {response_text}")
                # Fallback: try to extract numbers and use the whole response as reasoning
                match = re.search(r"([0-9.]+)\s*%", response_text)
                if match:
                    growth_rate = float(match.group(1)) / 100.0
                else:
                    match = re.search(r"([0-9.]+)", response_text)
                    growth_rate = float(match.group(1)) / 100.0 if match else 0.08
                dcf_value = None
                dcf_match = re.search(r"DCF Value\s*[:=]?\s*([0-9.]+)", response_text, re.IGNORECASE)
                if dcf_match:
                    dcf_value = float(dcf_match.group(1))
                reasoning = response_text
        except Exception as e:
            logger.error(f"LLM growth rate/DCf extraction failed: {e}")
            growth_rate = 0.08
            dcf_value = None
            reasoning = f"Defaulted to 8% growth rate due to LLM error: {e}"

        # Get target price from state if available
        target_price = state.get("target_price")

        valuation_report_str = f"DCF Value: {dcf_value if dcf_value is not None else 'N/A'}" + "\n" + f"Growth Rate: {growth_rate*100:.2f}%" + "\n" + f"Reasoning: {reasoning}"
        output_dict = {
            'valuation_report': valuation_report_str,
            'dcf_value': dcf_value,
            'growth_rate': growth_rate,
            'reasoning': reasoning,
            'fcf': fcf,
            'revenue': revenue,
            'ticker': ticker,
            'region': region,
            'stock_price': state.get('stock_price')
        }
        logger.debug(f"ValuationAgent output: {output_dict}")
        return output_dict

    return valuation_analyst_node
