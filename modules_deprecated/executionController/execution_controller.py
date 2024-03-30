from openai import OpenAI
from modules.listener.whisper_listener import WhisperListener
from modules.roles.chains_creator import (
    DummyChainCreator,
    FactoryChain,
    ChainQ_ACreator,
)
from langchain.chat_models import ChatOpenAI
import time

from modules.talker.talker import Talker


class ExecutionController:

    def __init__(self, openai: OpenAI):
        self._listener = WhisperListener()
        self.__chain_factory = FactoryChain()
        self.__llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")
        self.__chain_factory.reg_concrete_chain("q_a", ChainQ_ACreator())
        self.__chain_factory.reg_concrete_chain("finish", DummyChainCreator())
        self.__talker = Talker(openai)

    def _listen(self):
        print("Wake-up Whisper...")
        return self._listener.execute()

    def execute(self):
        request = self._listen()
        print("request: ", request)
        (
            chain_creator,
            request_enhanced,
        ) = self.__chain_factory.create_concrete_chain_creator(request, self.__llm)
        if not chain_creator and not request_enhanced:
            print("Undefined request")
            return
        print("requestEnhanced ", request_enhanced)
        if request_enhanced["req_type"] == "finish":
            print("Finish Execution")
            return
        response = chain_creator.execute(request_enhanced["req_text"], self.__llm)

        print("response: ", response)
        self.__talker.say(response)
        time.sleep(0.20)
        print("Main Execution finished")
