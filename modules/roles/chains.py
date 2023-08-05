from abc import ABC, abstractmethod
from langchain.chat_models import ChatOpenAI
from modules.functions.create_prompt import create_prompt
from modules.roles_templates.q_a_template import (
    human_q_a_template,
    system_q_a_template,
)
from langchain.schema.output_parser import StrOutputParser

from dotenv import load_dotenv

load_dotenv()


class ChainGeneral(ABC):
    @abstractmethod
    def execute_chain(self):
        pass


class MeetingChain(ChainGeneral):
    def __init__(self):
        pass

    def execute_chain(self):
        return "MeetingChain"


class Q_AChain(ChainGeneral):
    def __init__(self):
        self._llm = ChatOpenAI(temperature=0.1)

    def execute_chain(self, request: str):
        prompt = create_prompt(
            system_prompt=system_q_a_template,
            human_prompt=human_q_a_template,
            input_variables=["output"],
        )
        functions_chain = prompt | self._llm | StrOutputParser()
        response = functions_chain.invoke({"output": request})
        return response
