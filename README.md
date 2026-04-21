# AI_Test_Error_Analysis_Tool 
🔍机器视觉测试错误智能分析工具 —— 基于大语言模型（LLM）视觉能力，专门用于漏检（Omission）与过杀（Overkill）错误的自动化诊断。

## 📖 项目背景
在机器视觉测试流程中，模型产生的错误通常分为两类：  
  **漏检 (Omission)**：实际存在缺陷，但被误判为正常。  
  **过杀 (Overkill)**：实际正常，但被误判为缺陷（虚警）。  

传统分析模式依赖人工逐张核对，不仅效率低下且标准难以统一。本工具通过集成 Qwen-VL-Plus 大模型，实现对错误图片的自动化成因分析，显著提升测试闭环效率。
## ✨ 功能特性自动化处理：
1. 支持上传 ZIP 压缩包，自动完成解压与图片预处理。  
2. 双模式诊断：针对性分析“漏检”与“过杀”两种逻辑错误。  
3. 智能分析引擎：调用 通义千问 Qwen-VL-Plus 模型，深度理解图像语义。  
4. 结构化输出：分析结果以 JSON 格式 呈现，支持一键复制，方便对接缺陷管理系统。  
5. 现代 UI 交互：基于 Gradio 4.x 打造，具备美观的进度条提示与定制化 CSS 样式。
## 🛠️ 技术栈模块
1. 技术方案前端界面Gradio 4.x (自定义主题 + CSS 美化)  
2. 视觉模型通义千问 qwen-vl-plus (OpenAI SDK 兼容接口)  
3. 图像处理Pillow (PIL) + Base64   
4. 编码配置管理环境变量 + JSON 配置文件
## 📂 项目结构
```
PlaintextAI_Test_Error_Analysis_Tool/
├── ui/
│   └── temp/              # 运行缓存数据
├── output/
│   └── analysis_res.json  # AI 分析结果输出
├── data/
│   └── messages.json      # AI Prompt 提示词模板
├── config.py              # 全局参数配置
├── API_Aufruf.py          # 模型 API 调用封装
├── AItest.py              # 核心业务逻辑处理
├── readdata.py            # 数据解析与文件处理
├── tool_main.py           # Gradio Web 界面主程序
└── README.md              # 项目说明文档
```
## 🚀 快速开始
1. 环境准备：
```
Bashpip install gradio openai pillow
export DASHSCOPE_API_KEY="your_api_key_here"
```
2. 准备测试数据将待分析的图片（支持 .jpg, .png）打包为 ZIP 压缩包：
```
Plaintexttest_data.zip
├── img1.jpg
└── img2.png
```
3. 启动程序
`Bashpython tool_main.py`
运行成功后，在浏览器访问：http://localhost:7860
## 💡 使用说明
1. 数据上传：在界面上传准备好的 ZIP 压缩包。  
2. 模式选择：根据当前测试批次，选择 “漏检” 或 “过杀” 分析模式。  
3. 开始任务：点击 “开始分析”，系统将实时显示处理进度。  
4. 结果导出：分析结束后，在结果区域查看详细的 AI 诊断意见并进行复制。
## 🔧 扩展性说明
1. Prompt自定义：通过修改 data/messages.json 即可优化 AI 的分析维度和话术。  
2. 模型切换：本项目代码兼容 OpenAI SDK 规范，可在 config.py 中轻松切换至 GPT-4o 或其他国产大模型。  
3. 并发处理：支持多图并行处理，适应中大规模测试集分析。

-------------------------------------------------
👤 作者软件测试工程师 | 专注机器视觉测试与 AI 辅助分析

  工具开发注：本项目主要用于个人简历展示，体现 Gradio 快速原型开发、大模型 API 集成及复杂测试场景下的工程化解决能力。
