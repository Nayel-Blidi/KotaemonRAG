import os
from langchain_core.language_models.llms import LLM
import requests
import pprint
from typing import Any, List, Mapping, Optional
import websocket
import json
from contextlib import closing

from .base import BaseLLM
from kotaemon.base import BaseComponent, LLMInterface

from kotaemon.base import BaseMessage, HumanMessage, LLMInterface, Param
from uuid import uuid4

class CustomLLM(BaseLLM):
    provider: str = 'azure'
    model_name: str = 'openai.gpt-4o'
    session_id: str = str(uuid4())
    SOCKET_URL: str
    API_TOKEN: str
    temperature: float = 0.0
    maxTokens: int = 512

    api_key: str = Param(help="API key", required=True)

    _role_mapper: dict[str, str] = {
        "human": "user",
        "system": "system",
        "ai": "assistant",
    }

    @property
    def _llm_type(self) -> str:
        return "custom"

    def run(self, messages):
        return self._call(prompt=messages)


    def prepare_message(
        self, messages: str | BaseMessage | list[BaseMessage]
    ) -> list[dict]:
        input_: list[BaseMessage] = []

        print(messages)

        input_ = ""
        if isinstance(messages, str):
            input_ = messages #[HumanMessage(content=messages)]
        elif isinstance(messages, HumanMessage):
            input_ = messages.content
        if isinstance(messages, list):
            # messages = messages[0]
            for message in messages:
                if isinstance(message, HumanMessage):
                    input_ += f" {message.content}"
        else:
            input_ = messages

        # output_ = ' '.join([each.content for each in input_]) # flattens the AI, System, Human inputs into a single string 

        return str(input_)


    def _call(self, prompt: str) -> str:

        prompt = self.prepare_message(messages=prompt)
        print("\n", prompt, type(prompt), "\n")

        def send_query(ws, prompt):
            # model_interface = 'multimodal' if self.model_name.startswith('anthropic.claude-3') else 'langchain'
            model_interface = "langchain"
            data = {
                "action": "run",
                "modelInterface": model_interface,
                "data": {
                    "mode": "chain",
                    "text": prompt,
                    "files": [],
                    "modelName": self.model_name,
                    "provider": self.provider,
                    "sessionId": self.session_id,
                    "workspaceId": "",
                    "modelKwargs": {
                        "streaming": True,
                        "maxTokens": self.maxTokens,
                        "temperature": self.temperature,
                        "topP": 0.7
                    }
                }
            }
            ws.send(json.dumps(data))
            r1 = None
            while r1 is None:
                m1 = ws.recv()
                j1 = json.loads(m1)
                a1 = j1.get("action")
                if "final_response" == a1:
                    r1 = j1.get("data", {}).get("content")
                if "error" == a1:
                    print("M1:" + str(m1))
            return j1

        with closing(websocket.create_connection(self.SOCKET_URL, header={"x-api-key": self.api_key})) as ws:
            j1 = send_query(ws, prompt)
        
        output = j1['data']['content']


        return LLMInterface(content=output)#OutputMessage(content=output))


    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"provider": self.provider, "model_name": self.model_name, "session_id": self.session_id, 'SOCKET_URL': self.SOCKET_URL, 'API_TOKEN': '<hidden>', 'temperature': self.temperature}


class OutputMessage():

    def __init__(self, content: str):
        self.text = content
        self.content = content

    def to_openai_format(self, content):
        return {"role": "assistant", "content": content}
    
    def __repr__(self):
        return self.text
