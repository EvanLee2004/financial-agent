"""
AI_eyes_vlm - 使用 Qwen3-VL 视觉大模型替代 OCR 进行财务报表识别
"""
import json
import os
import base64
from typing import List, Sequence, Union
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
)


def _normalize_path(raw_path: str) -> str:
    """标准化路径"""
    cleaned = raw_path.strip().strip('"').strip("'")
    return os.path.abspath(os.path.expanduser(cleaned))


def _gather_image_paths(image_inputs: Union[str, Sequence[str]]) -> List[str]:
    """收集并验证图片路径"""
    if isinstance(image_inputs, str):
        image_inputs = [image_inputs]

    paths: List[str] = []
    seen = set()
    for raw_path in image_inputs:
        if not raw_path:
            continue
        path = _normalize_path(str(raw_path))
        if not os.path.isfile(path):
            raise FileNotFoundError(f"找不到图片: {path}")
        if os.path.splitext(path)[1].lower() not in {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}:
            raise ValueError(f"暂不支持的图片格式: {path}")
        if path not in seen:
            paths.append(path)
            seen.add(path)

    if not paths:
        raise ValueError("请提供至少一张图片路径")
    return paths


def _image_to_base64(path: str) -> str:
    """将图片转换为 Base64 编码"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _get_image_mime_type(path: str) -> str:
    """根据文件扩展名获取 MIME 类型"""
    ext = os.path.splitext(path)[1].lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".bmp": "image/bmp",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_types.get(ext, "image/jpeg")


# VLM Prompt - 告诉模型如何提取财务数据
VLM_SYSTEM_PROMPT = """你是一个专业的财务报表分析助手。请仔细查看用户提供的财务报表图片，提取关键信息并以 JSON 格式返回。

提取要求：
1. 识别报表类型：资产负债表、利润表、现金流量表
2. 识别报表期间（如：2024年12月31日）
3. 提取主要财务科目及其金额（期末余额、期初余额）
4. 对于表格数据，确保科目名称和金额对应正确

返回格式（严格遵循以下 JSON 结构）：
{
    "report_type": "资产负债表",
    "period": "2024年12月31日",
    "items": {
        "货币资金": [1234567.89, 987654.32],
        "应收账款": [2345678.90, 1987654.32],
        ...
    }
}

注意：
- items 中的每个科目对应一个数组 [期末余额, 期初余额]
- 金额只保留数字，不要包含逗号或单位
- 如果无法识别期初余额，用 null 表示
- 只返回 JSON 数据，不要添加其他说明文字"""


def _extract_with_vlm(image_path: str) -> dict:
    """使用 Qwen3-VL 模型提取图片中的财务数据"""
    # 初始化 VLM 客户端
    vlm = ChatOpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=4096,
    )

    # 读取图片并转为 base64
    base64_image = _image_to_base64(image_path)
    mime_type = _get_image_mime_type(image_path)

    # 构建消息
    message = HumanMessage(
        content=[
            {"type": "text", "text": VLM_SYSTEM_PROMPT},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}"
                }
            }
        ]
    )

    # 调用 VLM
    response = vlm.invoke([message])
    content = response.content

    # 解析 JSON 响应
    try:
        # 尝试直接解析
        data = json.loads(content)
    except json.JSONDecodeError:
        # 如果失败，尝试从文本中提取 JSON 部分
        try:
            # 查找 ```json 代码块
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                # 尝试查找花括号包裹的内容
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    json_str = content[start:end+1]
                else:
                    raise ValueError("无法从响应中提取 JSON")
            data = json.loads(json_str)
        except Exception as e:
            raise ValueError(f"解析 VLM 响应失败: {e}\n原始响应: {content}")

    return data


def _ai_eyes_vlm_impl(image_inputs: Union[str, Sequence[str]]) -> str:
    """使用 VLM 从一张或多张图片中提取财务数据"""
    paths = _gather_image_paths(image_inputs)
    total = len(paths)
    sequential_hint = (
        f"共收到 {total} 张图片，按顺序依次提取。\n" if total > 1 else ""
    )

    results: List[str] = []
    if sequential_hint:
        results.append(sequential_hint.rstrip())

    for idx, path in enumerate(paths, start=1):
        try:
            data = _extract_with_vlm(path)
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            results.append(
                f"第 {idx}/{total} 张提取成功 ({path}):\n结构化数据:\n{json_str}\n{'-'*60}"
            )
        except Exception as exc:
            results.append(f"第 {idx}/{total} 张失败 ({path}): {exc}")

    return "\n\n".join(results)


# 创建工具
AI_eyes = tool(_ai_eyes_vlm_impl)

__all__ = ["AI_eyes"]
