from abc import ABC, abstractmethod
from .model_responses import ModelResponse, MeetingResponse, Q_AResponse
from typing import Dict
from modules.langChain.lang_chain_brain import LangChainBrain


class CreatorRole(ABC):
    def __init__(self):
        self._modelResponse = None

    def generate_response(self, improved_req) -> str:
        self._modelResponse = self.factory_model_response()
        return self._modelResponse.process_req(improved_req)

    @abstractmethod
    def factory_model_response(self):
        pass


class FactoryRole:
    def __init__(self):
        self._creators = {}
        self._langChainBrain = LangChainBrain()

    def reg_concrete_role(self, request_type: str, creator: CreatorRole):
        self._creators[request_type] = creator

    def create_concrete_role(self, req_text: str) -> tuple[CreatorRole, Dict[str, str]]:
        requestEnhanced = self._langChainBrain.improve_listening(req_text)
        creator = self._creators.get(requestEnhanced.req_type)
        if not creator:
            raise ValueError(requestEnhanced)
        return creator, requestEnhanced


class MeetingCreator(CreatorRole):
    def factory_model_response(self) -> ModelResponse:
        return MeetingResponse()


class Q_ACreator(CreatorRole):
    def factory_model_response(self) -> ModelResponse:
        return Q_AResponse()
