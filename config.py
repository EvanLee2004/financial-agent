"""
Brain Storm - 财务分析 AI Agent 配置文件
所有可配置项集中管理，方便修改和环境切换
"""

# ============ LLM 配置 ============
LLM_BASE_URL = "http://127.0.0.1:8000/v1"
LLM_API_KEY = "lm-studio"
LLM_MODEL = "qwen2.5-vl-7b-instruct"
LLM_TEMPERATURE = 0.1

# ============ Agent 配置 ============
AGENT_MAX_ITERATIONS = 10
AGENT_VERBOSE = True
AGENT_HANDLE_PARSING_ERRORS = True

# ============ OCR 配置 ============
OCR_LANGUAGES = ['ch_sim', 'en']  # 简体中文和英文

# ============ Prompt 模板 ============
AGENT_PROMPT_TEMPLATE = """
你是一名专业的财务分析助手。
核心规则：
1. 你的任务是回答用户的财务问题或普通聊天。
2. 只有当用户**明确提供了图片文件路径**（例如：/Users/evan/report.png）时，你才被许使用工具。
3. 如果用户只输入了符号或模糊指令（如"分析一下"）但没给路径，**不需要调用工具**！你应礼貌地询问用户："请提供您想要分析的财务报表图片路径。"

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
