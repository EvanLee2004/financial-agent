from langchain.tools import tool
import easyocr
import os

# 初始化EasyOCR阅读器，指定中文
reader = easyocr.Reader(['ch_sim', 'en'])  # 简体中文和英文

@tool  # 【装饰器层】：贴上“工具”标签
def AI_eyes(image_path: str) -> str:  # 【函数定义层】：创建工具
    """
    从财务报表截图中提取结构化文本信息。该工具专门用于处理清晰的财务报表图片（如资产负债表、利润表）。

    **工作流程与特点**：
    1.  **输入**：接收一个本地图片文件路径（支持PNG、JPG等格式）。
    2.  **处理**：使用中英文OCR引擎识别图片中的文字，并**自动按行组织输出**。
    3.  **输出**：返回一个清晰的、分行显示的文本块，其中包含“科目名称”和对应的“金额”。
    4.  **数据特征**：识别出的金额数字可能包含千分位分隔符（如3,270,500.00）。表格中无数字的行表示该科目当期无发生额或余额为零。
    5.  **已知局限**：对**极模糊、低分辨率、手写体或复杂背景**的图片识别准确率会下降。目前**不支持直接处理PDF文件**，需先将PDF每页转为图片。

    **参数**：
    - image_path (str): 财务报表图片的本地绝对或相对路径。例如：'.test_data/图名.png'

    **返回**：
    - 一个字符串，格式为：'从图片中提取的文本内容如下：\\n\\n[识别出的文本]'
    - 如果发生错误，将返回错误描述字符串。

    **使用示例**（供参考如何调用）：
    - 用户请求：“分析一下 .test_data/report.png 这张资产负债表。”
    - AI应调用：`parse_financial_statement('.test_data/report.png')`
    """
    try:  # 【安全层】：开始尝试执行，准备捕获错误
        if not os.path.exists(image_path):  # 【安全检查】：先确认文件存在
            return f"错误：找不到文件 {image_path}，请检查路径。"  # 【错误反馈1】：文件不存在时，给AI明确的错误信息

        # 【核心工作】：调用OCR引擎干活
        result = reader.readtext(image_path, detail=0)  # 让配置好的reader识别图片，`detail=0`表示只返回文字列表，不要坐标等额外信息
        extracted_text = "\n".join(result)  # 将列表 ['文字1', '文字2'] 合并成 "文字1\n文字2" 的字符串

        # 【成功返回】：把提取好的文本包装后返回
        return f"从图片中提取的文本内容如下：\n\n{extracted_text}"

    except Exception as e:  # 【异常捕获】：如果上面任何一步出错（如文件损坏、非图片格式、OCR内部错误）
        return f"处理图片时发生错误：{str(e)}"  # 【错误反馈2】：将错误信息返回给AI，而不是让程序崩溃
    
# 在 tools.py 末尾添加
if __name__ == "__main__":
    test_image_path = "test_data/北京首都在线科技股份有限公司_01.png" # 换成你的图片
    result = AI_eyes.run(test_image_path)
    print("OCR测试结果:")
    print(result)