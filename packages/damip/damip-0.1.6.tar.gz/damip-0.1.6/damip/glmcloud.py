#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 03 17 20:05:20 2024

@project: damip
@author : kaiwei.li
@company: Digitopia Robotics Ltd.,Co.
"""

import json
from zhipuai import ZhipuAI

class Chatglm:
    
    # Initial
    def __init__(self):
        self.name = "Chatglm"
        self.__access = self.__load_access()
        self.__prompt = self.__load_prompt()
        self.__glm_client = ZhipuAI(api_key=self.__access)
        self.__glm_messages = [{"role": "system", "content": self.__prompt},]

    # singleton
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            Chatglm._instance = object.__new__(cls)
        return Chatglm._instance

    # load access from json file
    def __load_access(self):
        try:
            with open('/usr/local/param/t1_access.json', 'r') as json_file:
                access_data = json.load(json_file)#.encode(encoding='utf-8')
                access_keys = access_data['zhipuai_key']
                # print(access_keys)
            return access_keys
        except Exception as e:
            print(":) load access json file failed!")

    # load prompt from json file
    def __load_prompt(self):
        try:
            with open('/usr/local/param/t1_prompt.json', 'r') as json_file:
                prompt_data = json.load(json_file)#.encode(encoding='utf-8')
                prompt_vers = prompt_data['version']
                prompt_text = prompt_data['prompt']
            return prompt_text
        except Exception as e:
            print(":) load prompt json file failed!")

    # chatglm message history clear
    def clear(self):
        self.__glm_messages = [{"role": "system", "content": self.__prompt},]
        return

    # chatglm request
    def request(self, ask_rq):
        ask_01 = "有人向你提问<你是谁啊>，你应该怎么回答？请将回答通过声卡播放。"
        ask_02 = "我需要你<说生日快乐>，你可以做到吗？"
        ask_03 = "有人向你提问<世界上最大的陆地生物是什么>，你应该怎么回答？请将回答通过声卡播放。"
        ask_04 = "你听到<小孩子哭>的声音，你会怎么办？不要忘记给出函数命令。"
        ask_05 = "你面前有<一个老人摔倒了>，你会怎么办？不要忘记给出函数命令。"

        #self.__glm_messages.append({"role": "user", "content": ask_rq})
        self.__glm_messages = [{"role": "system", "content": self.__prompt},{"role": "user", "content": ask_rq}]

        # save the chatglm message to log file

        print(":) cloud server chatglm request:", ask_rq)

        response = self.__glm_client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.__glm_messages,
            top_p=0.7,
            temperature=0.95,
            #max_tokens=1024,
            #stream=True,
        )

        result = str(response.choices[0].message)
        print(":) cloud server chatglm response:", result)
        return result
