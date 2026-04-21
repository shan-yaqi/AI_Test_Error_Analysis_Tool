import os.path
import gradio as gr
import time
import os
import json
import shutil
import zipfile
from config import CONFIG
from datetime import datetime
from readdata import Readdata
from API_Aufruf import Apiaufruf
readdata = Readdata()
apiaufruf = Apiaufruf()

RAG_DIR = os.path.join(os.path.dirname(__file__), "rag_data")
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MESSAGE_PATH = BASE_PATH + r'\data\messages.json'

api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("请先设置 DASHSCOPE_API_KEY 环境变量")

def file_exist(file_input,error_type):
    if file_input is None:
        raise gr.Error("请先上传文件")  # 隐藏
    if error_type is None:
        raise gr.Error("请选择图片类型")

def file_extract(file_input,progress=gr.Progress()):
    """
    inputs:zip
    outputs:extract_path----temp
    """
    extract_path = "ui/temp"
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    progress(0.1, "文件获取成功")
    os.makedirs(extract_path)

    # 解压zip
    progress(0.2, "解压文件中...")
    with zipfile.ZipFile(file_input.name, 'r') as z:
        z.extractall(extract_path)
    progress(0.3, "文件解压成功")
    return extract_path

def file_path(error_type,extract_path):
    """
    inputs:error_type(miss/overkill)、extract_path
    outputs:omission_path、overkill_path
    """
    if error_type == "漏检":
        omission_path = extract_path
        overkill_path = None
        # return omission_path,gr.update(visible=False)
    else:
        overkill_path = extract_path
        omission_path = None
        # return gr.update(visible=False),overkill_path
    return omission_path, overkill_path

def file_analyze(file_input,error_type,progress=gr.Progress()):
    try:
        progress(0, "验证输入中...")
        file_exist(file_input,error_type)  # 文件是否存在
        extract_path = file_extract(file_input,progress=gr.Progress())  # 解压
        miss_over_path = file_path(error_type, extract_path)  # 获取文件路径
        omission_path = miss_over_path[0]
        overkill_path = miss_over_path[1]

        if error_type == "漏检":
            data = readdata.read_imgfile_OK(omission_path)
            messages = readdata.Combine_data(data, MESSAGE_PATH)
        else:
            data = readdata.read_imgfile_NG(overkill_path)
            messages = readdata.Combine_data(data, MESSAGE_PATH)  # 获取文件夹内图片信息
        progress(0.4, "图片读取完成")

        progress(0.6, "AI分析中，请稍候...")
        ergebnisse = apiaufruf.Api_aufruf(api_key, CONFIG["base_url"],
                                          CONFIG["model"], messages)  # ai分析
        progress(0.8)
        clean_res = str(ergebnisse).strip()
        if clean_res.startswith("```"):
            clean_res = clean_res.strip("`")
            if clean_res.startswith("json"):
                clean_res = clean_res[4:].strip()

        try:
            # 尝试解析并重新格式化，确保有缩进
            json_obj = json.loads(clean_res)
            final_output = json.dumps(json_obj, indent=2, ensure_ascii=False)
        except:
            # 如果解析失败，直接显示原字符串
            final_output = clean_res

        progress(0.9,"打印结果中...")

        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("output", exist_ok=True)
        outputname = rf"output/result_{time_str}.json"

        with open(outputname, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        progress(1, "分析完成！")
        return final_output

    except gr.Error:
        raise
    except Exception as e:
        raise gr.Error(f"文件处理失败: {str(e)}")

# ============ 自定义主题 ============
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="gray",
    font=gr.themes.GoogleFont("Noto Sans SC")
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
    block_title_text_size="*text_lg",
    block_border_width="1px",
    block_shadow="*shadow_drop"
)

def ui_create():
    with gr.Blocks(theme=theme,title="AI测试错误分析工具") as demo:
        gr.Markdown("""
            # AI测试错误分析工具
            ### 上传图片ZIP包，智能分析漏检/过杀原因
            """,
            elem_classes="header-text")

        with gr.Row():
                file_input = gr.File(
                    label="上传zip文件",
                    file_types=[".zip"],
                    type="filepath")
        with gr.Row():
            with gr.Column():  # left
                error_type = gr.Radio(
                    choices=["漏检", "过杀"],
                    label="错误类型",
                    info="漏检：实际NG判为OK | 过杀：实际OK判为NG"
                )
                btn_analyze = gr.Button(
                    "开始分析",
                    variant="primary",
                    size="lg")

        out_result = gr.Code(
            label="分析结果",
            language="json",
            interactive=False,
            lines=20
        )
        btn_analyze.click(
            file_analyze,
            inputs=[file_input, error_type],
            outputs=out_result)
    return demo

if __name__ == "__main__":
    demo = ui_create()
    demo.queue()
    demo.launch()
