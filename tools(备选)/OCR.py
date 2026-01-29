from langchain.tools import tool
import easyocr
import os
from config import OCR_LANGUAGES

# 初始化 EasyOCR 阅读器，从配置读取支持的语言
reader = easyocr.Reader(OCR_LANGUAGES)


@tool
def AI_eyes(image_path: str) -> str:
    """
    从财务报表截图中提取结构化文本信息。该工具专门用于处理清晰的财务报表图片（如资产负债表、利润表、现金流量表等）。

    **工作流程与特点**：
    1.  **输入**：接收一个本地图片文件路径（支持PNG、JPG等格式）。
    2.  **处理**：使用中英文OCR引擎识别图片中的文字，并**自动按行组织输出**。
    3.  **输出**：返回一个清晰的、分行显示的文本块，其中包含"科目名称"和对应的"金额"。
    4.  **数据特征**：识别出的金额数字可能包含千分位分隔符（如3,270,500.00）。表格中无数字的行表示该科目当期无发生额或余额为零。
    5.  **已知局限**：对**极模糊、低分辨率、手写体或复杂背景**的图片识别准确率会下降。目前**不支持直接处理PDF文件**，需先将PDF每页转为图片。

    **参数**：
    - image_path (str): 财务报表图片的本地绝对或相对路径。例如：'test_data/图名.png'

    **返回**：
    - 一个字符串，格式为：'从图片中提取的文本内容如下：\\n\\n[识别出的文本]'
    - 如果发生错误，将返回错误描述字符串。

    **使用示例**（供参考如何调用）：
    - 用户请求："分析一下 test_data/report.png 这张财务报表。"
    - AI应调用：`AI_eyes('test_data/report.png')`
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return f"错误：找不到文件 {image_path}，请检查路径。"

        # 调用 OCR 引擎识别图片
        result = reader.readtext(image_path, detail=0)
        extracted_text = "\n".join(result)

        return f"从图片中提取的文本内容如下：\n\n{extracted_text}"

    except Exception as e:
        return f"处理图片时发生错误：{str(e)}"


# 测试入口
if __name__ == "__main__":
    test_image_path = "test_data/北京首都在线科技股份有限公司_01.png"
    result = AI_eyes.run(test_image_path)
    print("OCR测试结果:")
    print(result)