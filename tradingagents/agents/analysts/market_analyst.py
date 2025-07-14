from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import time
import json


def create_market_analyst_react(llm, toolkit):
    """使用ReAct Agent模式的市场分析师（适用于通义千问）"""
    def market_analyst_react_node(state):
        print(f"📈 [DEBUG] ===== ReAct市场分析师节点开始 =====")

        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        print(f"📈 [DEBUG] 输入参数: ticker={ticker}, date={current_date}")

        # 检查是否为中国股票
        def is_china_stock(ticker_code):
            import re
            return re.match(r'^\d{6}$', str(ticker_code))

        is_china = is_china_stock(ticker)
        print(f"📈 [DEBUG] 股票类型检查: {ticker} -> 中国A股: {is_china}")

        if toolkit.config["online_tools"]:
            # 在线模式，使用ReAct Agent
            if is_china:
                print(f"📈 [市场分析师] 使用ReAct Agent分析中国股票")

                # 创建中国股票数据工具
                from langchain_core.tools import BaseTool

                class ChinaStockDataTool(BaseTool):
                    name: str = "get_china_stock_data"
                    description: str = f"获取中国A股股票{ticker}的市场数据和技术指标（优化缓存版本）。直接调用，无需参数。"

                    def _run(self, query: str = "") -> str:
                        try:
                            print(f"📈 [DEBUG] ChinaStockDataTool调用，股票代码: {ticker}")
                            # 使用优化的缓存数据获取
                            from tradingagents.dataflows.optimized_china_data import get_china_stock_data_cached
                            return get_china_stock_data_cached(
                                symbol=ticker,
                                start_date='2025-05-28',
                                end_date=current_date,
                                force_refresh=False
                            )
                        except Exception as e:
                            print(f"❌ 优化A股数据获取失败: {e}")
                            # 备用方案：使用原始API
                            try:
                                return toolkit.get_china_stock_data.invoke({
                                    'stock_code': ticker,
                                    'start_date': '2025-05-28',
                                    'end_date': current_date
                                })
                            except Exception as e2:
                                return f"获取股票数据失败: {str(e2)}"

                tools = [ChinaStockDataTool()]
                query = f"""请对中国A股股票{ticker}进行详细的技术分析。

执行步骤：
1. 使用get_china_stock_data工具获取股票市场数据
2. 基于获取的真实数据进行深入的技术指标分析
3. 直接输出完整的技术分析报告内容

重要要求：
- 必须输出完整的技术分析报告内容，不要只是描述报告已完成
- 报告必须基于工具获取的真实数据进行分析
- 报告长度不少于800字
- 包含具体的数据、指标数值和专业分析

报告格式应包含：
## 股票基本信息
## 技术指标分析
## 价格趋势分析
## 成交量分析
## 市场情绪分析
## 投资建议"""
            else:
                print(f"📈 [市场分析师] 使用ReAct Agent分析美股/港股")

                # 创建美股数据工具
                from langchain_core.tools import BaseTool

                class USStockDataTool(BaseTool):
                    name: str = "get_us_stock_data"
                    description: str = f"获取美股/港股{ticker}的市场数据和技术指标（优化缓存版本）。直接调用，无需参数。"

                    def _run(self, query: str = "") -> str:
                        try:
                            print(f"📈 [DEBUG] USStockDataTool调用，股票代码: {ticker}")
                            # 使用优化的缓存数据获取
                            from tradingagents.dataflows.optimized_us_data import get_us_stock_data_cached
                            return get_us_stock_data_cached(
                                symbol=ticker,
                                start_date='2025-05-28',
                                end_date=current_date,
                                force_refresh=False
                            )
                        except Exception as e:
                            print(f"❌ 优化美股数据获取失败: {e}")
                            # 备用方案：使用原始API
                            try:
                                return toolkit.get_YFin_data_online.invoke({
                                    'symbol': ticker,
                                    'start_date': '2025-05-28',
                                    'end_date': current_date
                                })
                            except Exception as e2:
                                return f"获取股票数据失败: {str(e2)}"

                class FinnhubNewsTool(BaseTool):
                    name: str = "get_finnhub_news"
                    description: str = f"获取美股{ticker}的最新新闻和市场情绪（通过FINNHUB API）。直接调用，无需参数。"

                    def _run(self, query: str = "") -> str:
                        try:
                            print(f"📈 [DEBUG] FinnhubNewsTool调用，股票代码: {ticker}")
                            return toolkit.get_finnhub_news.invoke({
                                'ticker': ticker,
                                'start_date': '2025-05-28',
                                'end_date': current_date
                            })
                        except Exception as e:
                            return f"获取新闻数据失败: {str(e)}"

                tools = [USStockDataTool(), FinnhubNewsTool()]
                query = f"""请对美股{ticker}进行详细的技术分析。

执行步骤：
1. 使用get_us_stock_data工具获取股票市场数据和技术指标（通过FINNHUB API）
2. 使用get_finnhub_news工具获取最新新闻和市场情绪
3. 基于获取的真实数据进行深入的技术指标分析
4. 直接输出完整的技术分析报告内容

重要要求：
- 必须输出完整的技术分析报告内容，不要只是描述报告已完成
- 报告必须基于工具获取的真实数据进行分析
- 报告长度不少于800字
- 包含具体的数据、指标数值和专业分析
- 结合新闻信息分析市场情绪

报告格式应包含：
## 股票基本信息
## 技术指标分析
## 价格趋势分析
## 成交量分析
## 新闻和市场情绪分析
## 投资建议"""

            try:
                # 创建ReAct Agent
                prompt = hub.pull("hwchase17/react")
                agent = create_react_agent(llm, tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    handle_parsing_errors=True,
                    max_iterations=10,  # 增加到10次迭代，确保有足够时间完成分析
                    max_execution_time=180  # 增加到3分钟，给更多时间生成详细报告
                )

                print(f"📈 [DEBUG] 执行ReAct Agent查询...")
                result = agent_executor.invoke({'input': query})

                report = result['output']
                print(f"📈 [市场分析师] ReAct Agent完成，报告长度: {len(report)}")

            except Exception as e:
                print(f"❌ [DEBUG] ReAct Agent失败: {str(e)}")
                report = f"ReAct Agent市场分析失败: {str(e)}"
        else:
            # 离线模式，使用原有逻辑
            report = "离线模式，暂不支持"

        print(f"📈 [DEBUG] ===== ReAct市场分析师节点结束 =====")

        return {
            "messages": [("assistant", report)],
            "market_report": report,
        }

    return market_analyst_react_node


def create_market_analyst(llm, toolkit):

    def market_analyst_node(state):
        print(f"📈 [DEBUG] ===== 市场分析师节点开始 =====")

        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        print(f"📈 [DEBUG] 输入参数: ticker={ticker}, date={current_date}")
        print(f"📈 [DEBUG] 当前状态中的消息数量: {len(state.get('messages', []))}")
        print(f"📈 [DEBUG] 现有市场报告: {state.get('market_report', 'None')[:100]}...")

        # 根据股票代码格式选择数据源
        from tradingagents.utils.stock_utils import StockUtils

        market_info = StockUtils.get_market_info(ticker)
        is_china = market_info['is_china']
        is_hk = market_info['is_hk']
        is_us = market_info['is_us']

        print(f"📈 [DEBUG] 股票类型检查: {ticker} -> {market_info['market_name']} ({market_info['currency_name']})")

        if toolkit.config["online_tools"]:
            # 使用统一的市场数据工具，工具内部会自动识别股票类型
            print(f"📊 [市场分析师] 使用统一市场数据工具，自动识别股票类型")
            tools = [toolkit.get_stock_market_data_unified]
            # 安全地获取工具名称用于调试
            tool_names_debug = []
            for tool in tools:
                if hasattr(tool, 'name'):
                    tool_names_debug.append(tool.name)
                elif hasattr(tool, '__name__'):
                    tool_names_debug.append(tool.__name__)
                else:
                    tool_names_debug.append(str(tool))
            print(f"📊 [DEBUG] 选择的工具: {tool_names_debug}")
            print(f"📊 [DEBUG] 🔧 统一工具将自动处理: {market_info['market_name']}")
        else:
            tools = [
                toolkit.get_YFin_data,
                toolkit.get_stockstats_indicators_report,
            ]

        # 统一的系统提示，适用于所有股票类型
        system_message = (
            f"""你是一位专业的股票技术分析师。你必须对股票{ticker} ({market_info['market_name']})进行详细的技术分析。

**工具调用指令：**
你有一个工具叫做get_stock_market_data_unified，你必须立即调用这个工具来获取股票{ticker}的数据。
不要说你将要调用工具，直接调用工具。

**分析要求：**
1. 调用工具后，基于获取的真实数据进行技术分析
2. 分析移动平均线、MACD、RSI、布林带等技术指标
3. 考虑市场特点进行分析
4. 提供具体的数值和专业分析
5. 给出明确的投资建议
6. 价格使用{market_info['currency_name']}（{market_info['currency_symbol']}）

**输出格式：**
## 📊 股票基本信息
## 📈 技术指标分析
## 📉 价格趋势分析
## 💭 投资建议

请使用中文，基于真实数据进行分析。"""
        )


        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是一位有用的AI助手，与其他助手协作。"
                    "使用提供的工具来回答问题。"
                    "如果你无法完全回答，没关系；另一位具有不同工具的助手"
                    "将从你停下的地方继续帮助。执行你能做的来取得进展。"
                    "如果你或任何其他助手有最终交易建议：**买入/持有/卖出**或可交付成果，"
                    "请在你的回复前加上'最终交易建议：**买入/持有/卖出**'，这样团队就知道要停止了。"
                    "你可以使用以下工具：{tool_names}。\n{system_message}"
                    "供你参考，当前日期是{current_date}。我们要分析的公司是{ticker}。请确保所有分析都使用中文。",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        # 安全地获取工具名称，处理函数和工具对象
        tool_names = []
        for tool in tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            elif hasattr(tool, '__name__'):
                tool_names.append(tool.__name__)
            else:
                tool_names.append(str(tool))

        prompt = prompt.partial(tool_names=", ".join(tool_names))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        # 处理市场分析报告
        if len(result.tool_calls) == 0:
            # 没有工具调用，直接使用LLM的回复
            report = result.content
            print(f"📊 [市场分析师] 直接回复，长度: {len(report)}")
        else:
            # 有工具调用，执行工具并生成完整分析报告
            print(f"📊 [市场分析师] 工具调用: {[call.get('name', 'unknown') for call in result.tool_calls]}")

            try:
                # 执行工具调用
                from langchain_core.messages import ToolMessage, HumanMessage

                tool_messages = []
                for tool_call in result.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_args = tool_call.get('args', {})
                    tool_id = tool_call.get('id')

                    print(f"📊 [DEBUG] 执行工具: {tool_name}, 参数: {tool_args}")

                    # 找到对应的工具并执行
                    tool_result = None
                    for tool in tools:
                        # 安全地获取工具名称进行比较
                        current_tool_name = None
                        if hasattr(tool, 'name'):
                            current_tool_name = tool.name
                        elif hasattr(tool, '__name__'):
                            current_tool_name = tool.__name__

                        if current_tool_name == tool_name:
                            try:
                                if tool_name == "get_china_stock_data":
                                    # 中国股票数据工具
                                    tool_result = tool.invoke(tool_args)
                                else:
                                    # 其他工具
                                    tool_result = tool.invoke(tool_args)
                                print(f"📊 [DEBUG] 工具执行成功，结果长度: {len(str(tool_result))}")
                                break
                            except Exception as tool_error:
                                print(f"❌ [DEBUG] 工具执行失败: {tool_error}")
                                tool_result = f"工具执行失败: {str(tool_error)}"

                    if tool_result is None:
                        tool_result = f"未找到工具: {tool_name}"

                    # 创建工具消息
                    tool_message = ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_id
                    )
                    tool_messages.append(tool_message)

                # 基于工具结果生成完整分析报告
                analysis_prompt = f"""现在请基于上述工具获取的数据，生成详细的技术分析报告。

要求：
1. 报告必须基于工具返回的真实数据进行分析
2. 包含具体的技术指标数值和专业分析
3. 提供明确的投资建议和风险提示
4. 报告长度不少于800字
5. 使用中文撰写

请分析股票{ticker}的技术面情况，包括：
- 价格趋势分析
- 技术指标解读
- 支撑阻力位分析
- 成交量分析
- 投资建议"""

                # 构建完整的消息序列
                messages = state["messages"] + [result] + tool_messages + [HumanMessage(content=analysis_prompt)]

                # 生成最终分析报告
                final_result = llm.invoke(messages)
                report = final_result.content

                print(f"📊 [市场分析师] 生成完整分析报告，长度: {len(report)}")

                # 返回包含工具调用和最终分析的完整消息序列
                return {
                    "messages": [result] + tool_messages + [final_result],
                    "market_report": report,
                }

            except Exception as e:
                print(f"❌ [市场分析师] 工具执行或分析生成失败: {e}")
                import traceback
                traceback.print_exc()

                # 降级处理：返回工具调用信息
                report = f"市场分析师调用了工具但分析生成失败: {[call.get('name', 'unknown') for call in result.tool_calls]}"

                return {
                    "messages": [result],
                    "market_report": report,
                }

        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
