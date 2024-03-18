from modules.listener.listener import Listener
from modules.roles.chains_creator import (
    FactoryChain,
    ChainQ_ACreator,
)
from langchain.chat_models import ChatOpenAI


class ExecutionController:
    def __init__(self):
        # self._listener = Listener()
        self.__chain_factory = FactoryChain()
        self.__llm = ChatOpenAI(temperature=0.3)
        self.__chain_factory.reg_concrete_chain("q_a", ChainQ_ACreator())

    def _listen(self):
        return self._listener.execute()

    def execute(self, request):
        # request = self._listen()
        # TODO: improve this when we want to have a conversation, not just a question
        (
            chain_creator,
            requestEnhanced,
        ) = self.__chain_factory.create_concrete_chain_creator(request, self.__llm)
        print("requestEnhanced ", requestEnhanced)
        response = chain_creator.execute(requestEnhanced["req_text"], self.__llm)
        print("response ", response)
