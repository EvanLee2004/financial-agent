from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools import AI_eyes  #  tools.py 在旁边

# --- 1. 连接模型 ---
llm = ChatOpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="lm-studio",
    model="qwen2.5-vl-7b-instruct",
    temperature=0.1,
)

# --- 2. 准备工具 ---
tools = [AI_eyes]

# --- 3. 提示词 (优化版) ---
template = """
你是一名专业的财务分析助手。
核心规则：
1. 你的任务是回答用户的财务问题或普通聊天。
2. 只有当用户**明确提供了图片文件路径**（例如：/Users/evan/report.png）时，你才被许使用工具。
3. 如果用户只输入了符号或模糊指令（如"分析一下"）但没给路径，**不需要调用工具**！你应礼貌地询问用户：“请提供您想要分析的财务报表图片路径。”

你可以使用的工具如下：
{tools}

遵守以下 ReAct 格式：

Question: 用户的提问
Thought: 
    (1) 用户有没有提供具体的文件路径？
    (2) 如果没有路径 -> 别想太多直接写 Final Answer回答用户。
    (3) 如果有路径 -> 决定调用 AI_eyes 工具。
Action: 如果需要工具，填 {tool_names} / 如果不需要不写
Action Input: 如果有 Action 填纯净路径字符串 / 否则不写
Observation:工具返回的结果

Thought: 
Final Answer: 最终回复内容

Question: {input}
Thought:{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

# --- 4. 组装 Agent ---
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# --- 5. 执行器 ---
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

# --- 6. 聊天循环 ---
print("--------------------------------------------------")
print("🔥 财报 Agent 已启动！(输入 q 退出)")
print("--------------------------------------------------")

while True:
    user_input = input("你: ").strip()
    if user_input.lower() in ("q", "quit", "退出"):
        break
    
    try:
        result = agent_executor.invoke({"input": user_input})
        print(f"\n🤖 财报专家: {result['output']}\n")
    except Exception as e:
        print(f"❌ 出错了: {str(e)}")