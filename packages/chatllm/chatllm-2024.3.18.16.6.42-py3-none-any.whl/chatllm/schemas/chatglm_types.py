#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatglm_types
# @Time         : 2024/3/11 20:10
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


class Part(BaseModel):
    """

    meta_data
        "metadata_list": [{
            "type": "webpage",
            "title": "南京天气预报,南京7天天气预报,南京15天天气预报,南京天气查询",
            "url": "http://www.weather.com.cn/weather/101190101.shtml",
            "text": "Web 结果1 天前 · 南京天气预报,南京7天天气预报,南京15天天气预报,南京天气查询. 预报. 全国 > 江苏 > 南京 > 城区. 18:00更新 | 数据来源 中央气象台. 今天. 7天. 8-15天. 40天. 雷达图. 2日（今天） 晴. 0℃. 3-4级. 3日（明天） 多云. 14℃ / 3℃. <3级转3-4级. 4日（后天） 阵雨转中雨. 13℃ / 7℃. <3级. 5日（周二） 阵雨转阴. 13℃ / 5℃. 4-5级. 6日（周 …   ",
            "pub_date": "1970-01-01T00:00:00.0000000"
        }]
    """
    id: str
    logic_id: str = ''
    role: str
    content: List[Dict[str, Any]]
    model: str
    recipient: str = ''
    created_at: str
    meta_data: dict = {}

    status: str

    # 预处理
    event: str = ''  # 类型
    markdown_data: str = ''

    def __init__(self, **data):
        super().__init__(**data)

        # self.event =
        # logger.debug(f"{self.status}: {self.content}")
        # logger.debug(
        #     f"""{self.status}: {self.content}\n{self.content and self.content[0].get("type")} \n {self.meta_data}""")
        # tool_calls image browser_result quote_result system_error
        if self.status == "finish" and self.content:
            # tool_calls
            if self.content[0].get("type") == "tool_calls":
                _ = self.content[0].get("tool_calls", {})
                if "mclick" not in str(_):
                    self.markdown_data += f"\n```json\n{_}\n```\n"

            if self.content[0].get("type") == "quote_result" and self.meta_data:
                # logger.debug(self.meta_data)
                for metadata in self.meta_data.get("metadata_list", []):
                    if metadata.get("type") == "webpage":
                        self.markdown_data += f"[🔗{metadata.get('title')}]({metadata.get('url')})\n\n"

            # code
            if self.content[0].get("type") == "code":
                code = self.content[0].get("code", "")
                self.markdown_data += f"""```{self.meta_data.get("toolCallRecipient", "python")}\n{code}\n```\n"""

            if self.content[0].get("type") == "execution_output":
                _ = self.content[0]
                self.markdown_data += f"\n```json\n{_}\n```\n"

                # image
            if self.content[0].get("type") == "image" and self.status == "finish":

                images = self.content[0].get("image", [])
                for image in images:
                    self.markdown_data += f"![image]({image['image_url']})\n\n"

        # text
        if self.content and self.content[0].get("type") == "text":
            # self.markdown_data = f"""<text>{self.content[0].get("text", "")}"""
            self.markdown_data = f"""{self.content[0].get("text", "")}"""


class Data(BaseModel):
    """
    {
        "id": "65eef45f3901fe6e0bb7153b",
        "conversation_id": "65eef45e3901fe6e0bb7153a",
        "assistant_id": "65940acff94777010aa6b796",
        "parts": [
            {
                "id": "65eef45f3901fe6e0bb7153b",
                "logic_id": "62a2d941-43ba-4a00-9933-4f2a18979201",
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "这是我为您创作的可爱猫咪图画，希望您喜欢。",
                        "status": "finish"
                    }
                ],
                "model": "chatglm-all-tools",
                "recipient": "all",
                "created_at": "2024-03-11 20:09:03",
                "meta_data": {
                    "toolCallRecipient": null
                },
                "status": "finish"  #
            }
        ],
        "created_at": "2024-03-11 20:09:03",
        "meta_data": {},
        "status": "finish",
        "last_error": {}
    }

    """
    id: str = "65940acff94777010aa6b796"  # chatglm4
    conversation_id: str
    assistant_id: str
    parts: List[Part]
    created_at: str
    status: str
    last_error: dict
