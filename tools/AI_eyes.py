import base64
import requests
from langchain.tools import tool
from config import LLM_BASE_URL, LLM_MODEL

def encode_image(image_path):
    """将图片转为 base64 编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@tool
def AI_eyes(image_path: str) -> str:
    """
    通过 Qwen3-VL 视觉大模型提取财务报表数据。
    它能自动识别表格结构，并以 Markdown 格式返回科目和金额。
    """
    try:
        base64_image = encode_image(image_path)
        
        # 构造符合 OpenAI 视觉格式的请求
        payload = {
            "model": LLM_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "你是一名资深会计。请识别这张财务报表图片，并将其内容提取为标准的 Markdown 表格。确保科目名称和金额（期末/期初）严格对应。"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            "temperature": 0.1
        }

        response = requests.post(f"{LLM_BASE_URL}/chat/completions", json=payload)
        response.raise_for_status()
        
        result = response.json()['choices'][0]['message']['content']
        return f"财报提取成功！以下是结构化数据：\n\n{result}"

    except Exception as e:
        return f"视觉识别失败: {str(e)}"