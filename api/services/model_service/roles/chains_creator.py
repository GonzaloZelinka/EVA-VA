from abc import ABC, abstractmethod

from api.utils.database_error import ToDatabaseException
from .chains import ChainGeneral, CreateToDoChain, MathChain, Q_AChain
from typing import Dict
from api.services.model_service.roles_templates.improve_listen_template import (
    human_improve_listening_template,
    system_improve_listening_template,
)
from api.services.model_service.roles_templates.q_a_template import (
    qa_system_subtask_template,
    qa_human_subtask_template,
)
from api.services.model_service.roles_templates.todo_template import (
    todo_system_subtask_template,
    todo_human_subtask_template,
)
from api.services.model_service.openai_functions.request_improve import improved_req_fn
from api.services.model_service.openai_functions.get_subtask import (
    get_subtask_q_a,
    get_subtask_todo,
)
from api.services.model_service.functions.create_prompt import create_prompt
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from dotenv import load_dotenv

load_dotenv()


class ChainCreator(ABC):
    def execute(self, improved_req, llm: ChatOpenAI) -> str:
        chain_type = self._identify_subtask(improved_req, llm)
        self.__chain = self._factory_chain(chain_type, llm)
        return self.__chain.execute_chain(improved_req)

    @abstractmethod
    def _factory_chain(self):
        pass

    @abstractmethod
    def _identify_subtask(self, improved_req):
        pass


class FactoryChain:
    def __init__(self):
        self.__creators = {}

    def reg_concrete_chain(self, request_type: str, creator: ChainCreator):
        self.__creators[request_type] = creator

    def create_concrete_chain_creator(
        self, req_text: str, llm: ChatOpenAI
    ) -> tuple[ChainCreator, Dict[str, str]]:
        prompt = create_prompt(
            system_prompt=system_improve_listening_template,
            human_prompt=human_improve_listening_template,
            input_variables=["output"],
        )
        functions_chain = (
            prompt
            | llm.bind(
                function_call={"name": "req_improved"}, functions=[improved_req_fn]
            )
            | JsonOutputFunctionsParser()
        )
        request_enhanced = functions_chain.invoke({"output": req_text})
        creator = self.__creators.get(request_enhanced["req_type"])
        if not creator:
            msg = f"Does not exist creator for request type: {request_enhanced['req_type']}"
            raise ToDatabaseException(msg, msg, 400)
        return creator, request_enhanced


class ChainQ_ACreator(ChainCreator):
    def _identify_subtask(self, improved_req, llm):
        prompt = create_prompt(
            system_prompt=qa_system_subtask_template,
            human_prompt=qa_human_subtask_template,
            input_variables=["output"],
        )
        functions_chain = (
            prompt
            | llm.bind(
                function_call={"name": "get_subtask_q_a"}, functions=[get_subtask_q_a]
            )
            | JsonOutputFunctionsParser()
        )

        subtask = functions_chain.invoke({"output": improved_req}).get("req_type")
        if subtask != "math" and subtask != "common":
            print(' "subtask" is not math or common', subtask)
            return None
        return subtask

    def _factory_chain(self, chain_type, llm) -> ChainGeneral:
        print("chain_type", chain_type)
        if chain_type == "math":
            return MathChain(llm)
        elif chain_type == "common":
            return Q_AChain(llm)


class DummyChainCreator(ChainCreator):
    def _identify_subtask(self, improved_req, llm):
        return None

    def _factory_chain(self, chain_type, llm) -> ChainGeneral:
        return None


class ChainToDoCreator(ChainCreator):

    def _identify_subtask(self, improved_req, llm):
        prompt = create_prompt(
            system_prompt=todo_system_subtask_template,
            human_prompt=todo_human_subtask_template,
            input_variables=["output"],
        )
        functions_chain = (
            prompt
            | llm.bind(
                function_call={"name": "get_subtask_todo"},
                functions=[get_subtask_todo],
            )
            | JsonOutputFunctionsParser()
        )

        subtask = functions_chain.invoke({"output": improved_req}).get("req_type")
        if (
            subtask != "create"
            and subtask != "delete"
            and subtask != "update"
            and subtask != "get"
        ):
            print(' "subtask" is not create, delete, update or get', subtask)
            return None

        return subtask

    def _factory_chain(self, chain_type, llm) -> ChainGeneral:
        print("chain_type", chain_type)
        if chain_type == "create":
            return CreateToDoChain(llm)
        # Should be done using a search chain
        # elif chain_type == "delete":
        #     return DeleteToDoChain(llm)
        # elif chain_type == "update":
        #     return UpdateToDoChain(llm)
        # elif chain_type == "get":
        #     return GetToDoChain(llm)
        return None
