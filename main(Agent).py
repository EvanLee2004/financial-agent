from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools import AI_eyes
from config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    AGENT_MAX_ITERATIONS,
    AGENT_VERBOSE,
    AGENT_HANDLE_PARSING_ERRORS,
    AGENT_PROMPT_TEMPLATE,
)

# --- 1. 连接模型 ---
llm = ChatOpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
)

# --- 2. 准备工具 ---
tools = [AI_eyes]

# --- 3. 提示词 ---
prompt = PromptTemplate.from_template(AGENT_PROMPT_TEMPLATE)

# --- 4. 组装 Agent ---
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# --- 5. 执行器 ---
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=AGENT_VERBOSE,
    handle_parsing_errors=AGENT_HANDLE_PARSING_ERRORS,
    max_iterations=AGENT_MAX_ITERATIONS,
)

# --- 6. 聊天循环 ---
if __name__ == "__main__":
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