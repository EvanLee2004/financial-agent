# 🔥 Brain Storm - 财务分析 AI Agent

基于 LangChain + Qwen3-VL 视觉大模型的智能财务报表分析助手。

## ✨ 功能特点

- 🤖 **智能对话**: 基于 ReAct 框架的 AI Agent，支持多轮对话记忆
- 👁️ **视觉识别**: 集成 Qwen3-VL 视觉模型，直接识别财务报表图片
- 📊 **结构化输出**: 自动将报表数据提取为 Markdown 表格格式
- 💬 **自然交互**: 智能判断何时调用工具，支持日常聊天

## 🛠️ 技术栈

- **LLM**: Qwen3-VL-30B (本地部署，通过 LM Studio)
- **框架**: LangChain + LangChain OpenAI
- **Agent**: ReAct Agent（推理+行动）
- **视觉**: OpenAI Vision API 格式 (Base64 图片)

## 📦 安装

1. 克隆仓库

```bash
git clone https://github.com/EvanLee2004/financial-agent.git
cd financial-agent
```

1. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

1. 安装依赖

```bash
pip install -r requirements.txt
```

1. 启动本地 LLM 服务
   - 使用 [LM Studio](https://lmstudio.ai/) 加载 Qwen3-VL 模型
   - 启动本地服务器（默认端口 8000）

## 🚀 使用方法

```bash
python main\(Agent\).py
```

示例对话：

```
你: 你好
🤖 财报专家: 你好！有什么财务问题我可以帮助你吗？

你: 分析一下 test_data/报表.png
🤖 财报专家: 财报提取成功！以下是结构化数据：
| 科目 | 期末余额 | 期初余额 |
|------|---------|---------|
| 货币资金 | 1,234,567 | 890,000 |
...
```

## 📁 项目结构

```
Brain storm/
├── main(Agent).py      # 主程序入口（命令行交互）
├── config.py           # 配置文件（LLM、Agent、Prompt）
├── tools/              # 工具模块
│   ├── AI_eyes.py      # 视觉识别工具（调用 VL 模型）
│   └── Calculater.py   # 计算工具（开发中）
├── test_data/          # 测试数据
├── requirements.txt    # 依赖列表
└── README.md
```

## ⚙️ 配置说明

在 `config.py` 中修改：

```python
LLM_BASE_URL = "http://127.0.0.1:8000/v1"  # LM Studio 地址
LLM_MODEL = "qwen/qwen3-vl-30b"            # 模型名称
```

## 📝 License

MIT
