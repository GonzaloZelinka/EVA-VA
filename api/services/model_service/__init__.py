from api.services.model_service.roles.chains_creator import (
    ChainQ_ACreator,
    DummyChainCreator,
    FactoryChain,
)
from langchain.chat_models import ChatOpenAI


class ModelService:
    def __init__(self):
        self.__chain_factory = FactoryChain()
        self.__llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")
        self.__chain_factory.reg_concrete_chain("q_a", ChainQ_ACreator())
        self.__chain_factory.reg_concrete_chain("finish", DummyChainCreator())

    def execute(self, request):
        chain_creator, request_enhanced = (
            self.__chain_factory.create_concrete_chain_creator(request, self.__llm)
        )
        if not chain_creator and not request_enhanced:
            return "Undefined request"
        if request_enhanced["req_type"] == "finish":
            return "Finish Execution"
        response = chain_creator.execute(request_enhanced["req_text"], self.__llm)
        return response
