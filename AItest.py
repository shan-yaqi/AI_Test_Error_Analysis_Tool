from readdata import Readdata
from API_Aufruf import Apiaufruf
from config import CONFIG
apiaufruf = Apiaufruf()
readdata = Readdata()
import os
from datetime import datetime
import json

# BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MESSAGE_PATH = BASE_PATH + r'\data\messages.json'

# API信息
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("请先设置 DASHSCOPE_API_KEY 环境变量")

def aitest(messages):
    ergebnisse = apiaufruf.Api_aufruf(api_key,CONFIG["base_url"],
                                      CONFIG["model"],messages)
    return ergebnisse

    # time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    # os.makedirs("output", exist_ok=True)
    # outputname = rf"output/result_{time_str}.json"
    #
    # with open(outputname, "w", encoding="utf-8") as f:
    #     json.dump(ergebnisse, f, indent=2, ensure_ascii=False)




