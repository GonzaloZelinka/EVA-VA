from abc import ABC, abstractmethod
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMMathChain
from langchain.schema.output_parser import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from api.services.model_service.functions.create_prompt import create_prompt
from api.services.model_service.roles_templates.q_a_template import (
    human_q_a_template,
    system_q_a_template,
)
from api.services.model_service.roles_templates.todo_template import (
    todo_human_subtask_template,
    todo_system_subtask_template,
)
from api.services.model_service.openai_functions.todo import (
    get_create_todo,
)
from dotenv import load_dotenv

load_dotenv()


class ChainGeneral(ABC):
    @abstractmethod
    def execute_chain(self):
        pass


class Q_AChain(ChainGeneral):
    def __init__(self, llm: ChatOpenAI):
        self.__llm = llm

    def execute_chain(self, request: str):
        prompt = create_prompt(
            system_prompt=system_q_a_template,
            human_prompt=human_q_a_template,
            input_variables=["output"],
        )
        chain = prompt | self.__llm | StrOutputParser()
        response = chain.invoke({"output": request})
        return response


class MathChain(ChainGeneral):
    def __init__(self, llm: ChatOpenAI):
        self.__llm = LLMMathChain.from_llm(llm)

    def execute_chain(self, request: str):
        response = self.__llm.run(request)
        return response.replace("Answer: ", "")


class CreateToDoChain(ChainGeneral):
    def __init__(self, llm: ChatOpenAI):
        self.__llm = llm

    def execute_chain(self, request: str):
        prompt = create_prompt(
            system_prompt=todo_system_subtask_template,
            human_prompt=todo_human_subtask_template,
            input_variables=["output"],
        )
        chain = (
            prompt
            | self.__llm.bind(
                function_call={"name": "get_create_todo"}, functions=[get_create_todo]
            )
            | JsonOutputFunctionsParser()
        )
        response = chain.invoke({"output": request})
        return response
