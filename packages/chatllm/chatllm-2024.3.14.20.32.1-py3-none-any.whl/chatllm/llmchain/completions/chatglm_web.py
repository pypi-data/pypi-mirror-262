#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatglm_web
# @Time         : 2024/3/11 18:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm 🧩 🔨[🔨](…….)
# @Description  : https://github.com/ikechan8370/chatgpt-plugin/blob/32af7b9a74fdfbd329f5977c6e3fb5b3928ed0f1/client/ChatGLM4Client.js#L6

from meutils.pipe import *
from meutils.notice.feishu import send_message

from chatllm.schemas import chatglm_types
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest
from chatllm.utils.openai_utils import openai_response2sse


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.access_token = self.get_access_token(self.api_key)

        self.httpx_client = httpx.Client(headers=self.headers, follow_redirects=True)
        self.httpx_aclient = httpx.AsyncClient(headers=self.headers, follow_redirects=True)

    # def create(self):
    #
    #     self.httpx_client.post(url, json={})

    def create(self, request: ChatCompletionRequest):
        request = self.do_request(request)

        url = "https://chatglm.cn/chatglm/backend-api/assistant/stream"
        payload = isinstance(request, dict) and request or request.model_dump()
        # response = self.httpx_client.post(url=url, json=payload)
        response: httpx.Response
        with self.httpx_client.stream("POST", url=url, json=payload, timeout=200) as response:

            content = ""
            for chunk in response.iter_lines():
                for chat_completion_chunk in self.do_chunk(chunk):
                    _ = chat_completion_chunk.choices[0].delta.content
                    chat_completion_chunk.choices[0].delta.content = _.split(content)[-1] if content else _
                    yield chat_completion_chunk
                    content = _

    async def acreate(self, request: Union[dict, ChatCompletionRequest]):
        request = self.do_request(request)

        url = "https://chatglm.cn/chatglm/backend-api/assistant/stream"
        payload = isinstance(request, dict) and request or request.model_dump()
        # response = self.httpx_client.post(url=url, json=payload)
        response: httpx.Response
        async with self.httpx_aclient.stream("POST", url=url, json=payload, timeout=200) as response:
            content = ""
            async for chunk in response.aiter_lines():
                for chat_completion_chunk in self.do_chunk(chunk):
                    _ = chat_completion_chunk.choices[0].delta.content
                    chat_completion_chunk.choices[0].delta.content = _.split(content)[-1] if content else _
                    yield chat_completion_chunk
                    content = _

    def create_sse(self, request: ChatCompletionRequest):
        if request.stream:
            return openai_response2sse(self.acreate(request), redirect_model=request.model)
        else:
            _chat_completion = chat_completion.model_copy(deep=True)
            _chat_completion.usage.prompt_tokens = len(request.messages[-1]["content"])
            for i in self.create(request):
                _chat_completion.choices[0].message.content += i.choices[0].delta.content

            return openai_response2sse(_chat_completion, redirect_model=request.model)

    def do_chunk(self, chunk):

        if chunk := chunk.strip().strip("event:message\ndata: ").strip():

            # logger.debug(chunk)

            chunk = chatglm_types.Data.model_validate_json(chunk)
            content = chunk.parts and chunk.parts[0].markdown_data
            if content:
                # logger.debug(content)
                # yield content
                chat_completion_chunk.choices[0].delta.content = content
                yield chat_completion_chunk

            if chunk.status == 'finish':
                _ = chat_completion_chunk.model_copy(deep=True)
                _.choices[0].delta.content = ""
                _.choices[0].finish_reason = "stop"  # 特殊
                yield _
                return

    def do_request(self, request: ChatCompletionRequest):

        history = request.messages[:-1]
        history = history and f"""参考系统历史对话，以聊天的语气回答问题：\n```json\n{json.dumps(history, ensure_ascii=False, indent=4)}\n```"""  # todo: 优化

        question = request.messages[-1]["content"]
        if isinstance(question, list):  # todo: 兼容多模态
            # 文件  {"type": "image_url", "image_url": {"url": image_url1}}
            # {
            #     "type": "http://ai.chatfire.cn/files/document/绩效面谈表-模版-nine-1710139239100-nine-66b3829d5.pdf text"
            # }

            send_message(request.messages)

        request.messages = [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': f"""{history}\n\n问题：{question}""" if history else question
                    }
                ]
            }
        ]

        logger.debug(request)

        return request

    def file_extract(self):
        """
        {
          "message": "success",
          "result": {
            "file_id": "chatglm4/f960da34-0041-4662-96e7-791ea455618a.png",
            "file_name": "8E8F00E40FED35D93339FF66691017CC.png",
            "file_size": 0,
            "file_url": "https://sfile.chatglm.cn/chatglm4/f960da34-0041-4662-96e7-791ea455618a.png",
            "height": 1024,
            "width": 1024
          },
          "status": 0
        }
        :return:
        """
        url = "https://chatglm.cn/chatglm/backend-api/assistant/file_upload"
        pass

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {self.access_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

    @staticmethod
    @ttl_cache(3600 * 2)
    def get_access_token(refresh_token=None):  # 设计重试
        refresh_token = refresh_token or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDE0OTU3OCwianRpIjoiYmQ3YWI2ZDItNWViNS00YmVmLTlmMWMtYzU5NTMwM2IyN2ZkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIzNmE4NmM1Yzc2Y2Q0MTcyYTE5NGYxMjQwZTgyMmIwOSIsIm5iZiI6MTcxMDE0OTU3OCwiZXhwIjoxNzI1NzAxNTc4LCJ1aWQiOiI2NDRhM2QwY2JhMjU4NWU5MDQ2MDM5ZGIiLCJ1cGxhdGZvcm0iOiIiLCJyb2xlcyI6WyJ1bmF1dGhlZF91c2VyIl19.gN8ci_OO8Pp0t3wZ3v1lG2X1xoLgGushf3fkm5pRl0M"

        headers = {
            'Authorization': f"Bearer {refresh_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        url = "https://chatglm.cn/chatglm/backend-api/v1/user/refresh"
        response = httpx.post(url, headers=headers)

        # logger.debug(refresh_token)
        # logger.debug(response.text)
        # logger.debug(response.status_code)

        if response.status_code != 200:
            send_message(f"GLM refresh_token:\n\n{response.text}\n\n{refresh_token}", title="GLM")
            response.raise_for_status()

        # refresh_token = response.get("refresh_token") # 是否去更新
        return response.json().get("result", {}).get("accessToken")


if __name__ == '__main__':
    # print(Completions.get_access_token())

    # data = {
    #     "assistant_id": "65940acff94777010aa6b796",
    #     "conversation_id": "",
    #     # "conversation_id": "",
    #     # "meta_data": {
    #     #     "is_test": False,
    #     #     "input_question_type": "xxxx",
    #     #     "channel": "",
    #     #     "draft_id": ""
    #     # },
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     # "text": "你是一个资深民商事律师，请你运用联网功能，帮我解决以下问题：\n压岁钱的所有权归谁，父母是否有权支配孩子压岁钱？\n请帮我写出相关法条和判例。",
    #                     # "text": "南京今天天气"
    #                     # "text": "画只猫"
    #                     # "text": "1+2"
    #                     "text": "总结一下 http://www.weather.com.cn/weather/101190101.shtml"
    #
    #                 }
    #             ]
    #         }
    #
    #     ]
    # }

    data = {
        "assistant_id": "65940acff94777010aa6b796",
        "conversation_id": "",
        # "conversation_id": "",
        # "meta_data": {
        #     "is_test": False,
        #     "input_question_type": "xxxx",
        #     "channel": "",
        #     "draft_id": ""
        # },
        "messages": [
            {
                "role": "user",
                "content": "讲个故事"
            }

        ]
    }

    for i in Completions().create(ChatCompletionRequest(**data)):
        print(i.choices[0].delta.content, end="")
        # pass
