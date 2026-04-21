# AI_Test_Error_Analysis_Tool
AI-Test-Demo: 机器视觉测试错误智能分析工具
基于大模型视觉能力的机器视觉测试错误原因分析工具，支持漏检/过杀错误的智能诊断。

项目背景
在机器视觉测试工作中，模型产生的错误分为两类：
漏检（Omission）：实际存在缺陷，但被误判为正常
过杀（Overkill）：实际正常，但被误判为缺陷
传统方式需要人工逐张查看图片并分析原因，效率低下。本工具利用大模型视觉能力，自动分析错误图片并给出可能的原因，显著提升测试分析效率。

功能特性
上传ZIP压缩包，自动解压并识别图片
支持漏检/过杀两种错误类型分析
调用通义千问视觉模型（qwen-vl-plus）智能分析错误原因
JSON格式结果输出，支持复制
美观的Gradio Web界面，带进度提示

技术栈
前端界面：Gradio 4.x（主题定制 + CSS美化）
视觉模型：通义千问 qwen-vl-plus（通过OpenAI SDK兼容接口调用）
图像处理：PIL + base64编码
配置管理：环境变量 + JSON配置文件

项目结构
AI_Test_Error_Analysis_Tool/
├── ui/
│   └── temp/              # 缓存数据
│── output/
│   └── xxx.json             # 分析结果输出
├── data/
│   └── messages.json        # AI提示词模板
├── config.py                # 配置文件
├── API_Aufruf.py           # API调用模块
├── AItest.py               # AI测试模块
├── readdata.py             # 数据处理模块
├── tool_main.py           # UI主界面显示
└── README.md

快速开始
1. 环境准备
# 安装依赖
pip install gradio openai pillow

# 配置API Key
export DASHSCOPE_API_KEY="your_api_key_here"

2. 准备测试数据
将测试图片按以下结构打包为ZIP：
test_data.zip
├── img1.jpg       
└── img2.png

3. 运行程序
cd ui
python app_beautified.py

浏览器访问 http://localhost:7860 即可使用。
使用说明
上传包含 ok/ 或 ng/ 图片的ZIP压缩包
选择错误类型（漏检/过杀）
点击"开始分析"按钮
等待AI分析完成，结果以JSON格式展示

扩展性
支持 messages.json 自定义提示词模板
可切换其他视觉模型（修改 config.py）
支持批量处理多张图片

作者
软件测试工程师 | 专注机器视觉测试与AI辅助分析


本项目用于简历项目展示，展示Gradio界面开发与大模型API集成能力
