import os
import json

class Readdata:
    def read_imgfile_OK(self, Omission_path):
        valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
        data = []

        for root, dirs, files in os.walk(Omission_path):
            for img in files:
                if img.lower().endswith(valid_ext):
                    full_path = os.path.join(root, img)

                    data.append({
                        "img": full_path,
                        "img_name": img,
                        "result": "NG",
                        "pro": "OK"  # model result,漏检
                    })
        return data

    def read_imgfile_NG(self, Overkill_path):
        valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
        data = []
        for root, dirs, files in os.walk(Overkill_path):
            for img in files:
                if img.lower().endswith(valid_ext):
                    full_path = os.path.join(root, img)
                    data.append({
                        "img": full_path,
                        "img_name": img,
                        "result":"OK",
                        "pro":"NG"
                    })
        return data

    def read_aimessage(self, MESSAGE_PATH: str):
        """
            读取json文件内容
        """
        with open(MESSAGE_PATH, "r", encoding="utf-8") as f:
            message = json.load(f)
        return message

    def Combine_data(self, data, MESSAGE_PATH):
        """
        合并数据，将图片文件和json文件内容合并
        :param data: 图片文件
        :param message_data: json文件内容
        :return: 合并后的数据
        """
        try:
            message = self.read_aimessage(MESSAGE_PATH)
            
            messages = []
            system_prompt = message.get("system")
            if isinstance(system_prompt, str) and system_prompt.strip():
                messages.append({"role": "system", "content": system_prompt})

            for item in data:
                messages.append({
                    "role": "user",
                    "content": message["user_template"].format(img=item["img"],img_name=item["img_name"],
                            pro=item["pro"],result=item["result"])
                })
            if not messages:
                raise ValueError("生成的 messages 为空")
            # 兼容接口约束：最后一条必须是 user/function/tool
            if messages[-1].get("role") not in ("user", "function", "tool"):
                raise ValueError(f"最后一条消息 role 非法：{messages[-1].get('role')}")
            return messages
        except Exception as e:
            print(f"错误信息：{e}")
            return None

    
            
