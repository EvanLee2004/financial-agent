from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools.AI_eyes_vlm import AI_eyes
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage

from config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
)

# 定义状态类
class FinancialState(TypedDict):
    messages: Annotated[List[BaseMessage], "add_messages"]  # 消息历史


SYSTEM_PROMPT = """
你是专业的财务报表分析专家,熟悉中国企业会计准则(CAS)。

回答原则：
- 所有数据须来自工具提取，绝不编造数字
- 语气专业亲切，像给朋友讲解财报
- 使用 Markdown 表格、加粗重点、列表呈现分析
- 结论要有洞察，不是简单罗列数字

工具使用规则：
目前工具：
1. AI_eyes: 用于从一张或多张图片中提取财务报表数据，返回 JSON 格式的结构化数据（多张用分隔线）。
   示例调用: image_paths = ["/Users/xx/报表1.png", "/Users/xx/报表2.png"]

在决定是否以及调用哪个工具之前，你必须在**内部**完整思考以下问题（不要把这些问题输出给用户）：
1. 用户真正的意图是什么？（是闲聊、问概念，还是要分析具体报表？）
2. 我目前缺少哪些关键信息？
3. 数据源是图片优先用AI_eyes。
4. 是否需要调用工具？如果需要，参数应精确填写成什么？
5. 工具返回后，我下一步要做什么？（直接回答）

遵守以上思考流程，然后再决定行动或直接给出最终回答。
"""

SYSTEM_MESSAGE = SystemMessage(content=SYSTEM_PROMPT.strip())

# --- 1. 连接模型 ---
llm = ChatOpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
)

# --- 2. 准备工具 ---
tools = [AI_eyes]  # 暂时只用AI_eyes

# --- 3. 创建LLM with tools ---
llm_with_tools = llm.bind_tools(tools)

# --- 4. 定义节点 ---
def agent_node(state: FinancialState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# --- 4. 构建图 ---
graph = StateGraph(FinancialState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", lambda x: "tools" if x["messages"][-1].tool_calls else END)
graph.add_edge("tools", "agent")

compiled_graph = graph.compile()
INVOCATION_CONFIG = {"recursion_limit": 100}

# --- 5. 聊天循环 ---
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("🔥 财报 Agent 已启动！(输入 q 退出)")
    print("--------------------------------------------------")

    # 初始状态
    initial_state = {"messages": [SYSTEM_MESSAGE]}

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ("q", "quit", "退出"):
            break
        
        try:
            # 添加用户消息
            initial_state["messages"].append(HumanMessage(content=user_input))
            
            # 执行图
            result = compiled_graph.invoke(initial_state, config=INVOCATION_CONFIG)
            
            # 获取AI回答
            ai_message = result["messages"][-1]
            answer = ai_message.content
            print(f"\n🚀 财报专家: {answer}\n")
            
            # 更新状态
            initial_state = result
            
        except Exception as e:
            print(f"❌ 出错了: {str(e)}")