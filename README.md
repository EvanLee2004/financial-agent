# 🔥 Brain Storm - 财务分析 AI Agent

一个基于 LangChain 和 Qwen2.5-VL 的智能财务报表分析助手。

## ✨ 功能特点

- 🤖 **智能对话**: 基于 ReAct 框架的 AI Agent，能够理解用户意图并自动决策
- 👁️ **视觉分析**: 集成 Qwen2.5-VL 多模态模型，可直接识别财务报表图片
- 📊 **专业解读**: 提供专业的财务数据解读和分析建议

## 🛠️ 技术栈

- **LLM**: Qwen2.5-VL-7B (本地部署)
- **框架**: LangChain + LangChain OpenAI
- **Agent**: ReAct Agent

## 📦 安装

1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/brain-storm.git
cd brain-storm
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

## 🚀 使用方法

1. 确保本地 LLM 服务正在运行（默认端口：8000）

2. 运行 Agent

```bash
python main\(Agent\).py
```

1. 开始对话

```
你: 请帮我分析这张财务报表 /path/to/your/report.png
🤖 财报专家: [分析结果]
```

## 📁 项目结构

```
Brain storm/
├── main(Agent).py     # 主程序入口
├── tools.py           # AI 工具定义
├── config.py          # 配置文件
├── requirements.txt   # 依赖列表
└── test_data/         # 测试数据
```

## 📝 License

MIT
