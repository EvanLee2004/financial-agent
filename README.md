# 🔥 Brain Storm - 财务分析 AI Agent

基于 LangChain + Qwen3-VL 视觉大模型的智能财务报表分析助手。

## ✨ 功能特点

- 🤖 **智能对话**: 通过 ReAct Agent 把语言推理和工具调用融合在一个回合里
- 👁️ **视觉识别**: `AI_eyes` 基于 Qwen3-VL 视觉大模型直接理解图片内容，输出结构化财务数据
- 🧮 **工具库**: `calculater.calculate_financial_ratios` 能将结构化报表（JSON）转成各类财务指标
- 💬 **自然交互**: 识别用户意图，只有在真正需要提取图表数据时才触发视觉工具，日常聊天无需多余动作

- **LLM**: Qwen3-VL (本地部署，通过 LM Studio)
- **框架**: LangChain + LangGraph
- **Agent**: ReAct Agent（推理+行动）
- **视觉**: OpenAI Vision API 格式 (Base64 图片)
- **数据处理**: Pandas（用于 `calculate_financial_ratios` 推算财务指标）

## 📦 安装

1. 克隆仓库

```bash
git clone https://github.com/EvanLee2004/financial-agent.git
cd financial-agent
```

2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 启动本地 LLM 服务
   - 使用 [LM Studio](https://lmstudio.ai/) 加载 **Qwen3-VL** 模型（支持视觉的多模态模型）
   - 启动本地服务器（默认端口 8000）
   - 确保 `config.py` 中的 `LLM_BASE_URL` 与 LM Studio 端口一致

## 🚀 使用方法

```bash
python main_agent.py
```

示例对话：

```
你: 你好
🤖 财报专家: 你好！有什么财务问题我可以帮助你吗？

你: 分析一下 test_data/北京首都在线科技股份有限公司_01.png
🤖 财报专家: 财报提取成功！以下是结构化数据：
| 科目 | 期末余额 | 期初余额 |
|------|---------|---------|
| 货币资金 | 1,234,567 | 890,000 |
...
```

## 📁 项目结构

```
Brain storm/
├── main_agent.py       # 主程序入口（命令行交互）
├── config.py           # 配置文件（LLM、Agent、Prompt）
├── tools/              # 工具模块
│   ├── AI_eyes_vlm.py  # 视觉识别工具（基于 Qwen3-VL 视觉模型）
│   └── calculater.py   # 财务指标计算器（基于 Pandas）
├── test_data/          # 测试数据
├── requirements.txt    # 依赖列表
└── README.md
```

## 🧰 工具模块说明

- **AI_eyes_vlm**: 调用 Qwen3-VL 视觉大模型直接理解图片内容，提取财务报表数据并输出结构化 JSON（包含报表类型、期间、主要科目数值）供 Agent 后续分析
- **calculate_financial_ratios** (tools/calculater.py): 依赖 Pandas，把结构化报表 JSON 转成 DataFrame，计算毛利率、ROE/ROA、偿债比率、周转率等指标，并返回一个 Markdown 报表

## ⚙️ 配置说明

在 `config.py` 中可以调整：

```python
LLM_BASE_URL = "http://127.0.0.1:8000/v1"  # LM Studio 地址（注意端口要与 LM Studio 一致）
LLM_MODEL = "qwen/qwen3-vl-8b"             # 模型名称
LLM_TEMPERATURE = 0.1                       # 控制响应随机性（0-1，越低越确定）
```

## 🔄 版本更新

### v2.0 - 视觉模型升级
- ✅ 将 OCR (EasyOCR) 替换为 Qwen3-VL 视觉大模型
- ✅ 提升复杂财务报表识别准确率
- ✅ 简化依赖，移除 OCR 相关库
