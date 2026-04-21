from openai import OpenAI
from readdata import Readdata
readdata = Readdata()

class Apiaufruf:
    def Api_aufruf(self,api_key,base_url,model,messages):
        """
        调用API
        :param api_key: API密钥
        :param base_url: API地址
        :param model: 模型名称
        :return: 返回API返回的结果
        """
        Ergebnisse = ""
        try:
            client = OpenAI(
                # api_key=os.getenv("DASHSCOPE_API_KEY"),
                # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key=api_key,
                base_url=base_url,
            )

            completion = client.chat.completions.create(
                model=model,
                messages=messages
            )
            Ergebnisse = completion.choices[0].message.content
            print(completion.choices[0].message.content)
        except Exception as e:
            print(f"错误信息：{e}")
        return  Ergebnisse