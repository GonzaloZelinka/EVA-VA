from modules.listener.whisper_listener import WhisperListener
from modules.roles.chains_creator import FactoryChain, ChainQ_ACreator, ChainEndCreator
from langchain.chat_models import ChatOpenAI
import time


class ExecutionController:
    def __init__(self):
        self._listener = WhisperListener()
        self.__chain_factory = FactoryChain()
        self.__llm = ChatOpenAI(temperature=0.3)
        self.__chain_factory.reg_concrete_chain("q_a", ChainQ_ACreator())
        self.__chain_factory.reg_concrete_chain("finish", ChainEndCreator())

    def _listen(self):
        return self._listener.execute()

    def execute(self):
        while True:
            request = self._listen()
            (
                chain_creator,
                request_enhanced,
            ) = self.__chain_factory.create_concrete_chain_creator(request, self.__llm)
            print("requestEnhanced ", request_enhanced)
            if request_enhanced["req_type"] == "finish":
                break
            response = chain_creator.execute(request_enhanced["req_text"], self.__llm)
            print("response ", response)
            time.sleep(0.20)
