from typing import Dict
import dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from modules.schemas.improved_req_schema import response_schemas
from modules.roles_templates.listener_template import (
    human_improve_listening_template,
    system_improve_listening_template,
)

dotenv.load_dotenv()


class LangChainBrain:
    def __init__(self) -> None:
        self._general_llm = ChatOpenAI(temperature=0.1)
        self._complex_llm = ChatOpenAI(temperature=0.1, model="gpt4")

    def improve_listening(self, input) -> Dict[str, str]:
        # TODO: we need to add a agent that can handle a search in a database to find for example the "team" and give the emails and after create the meeting.
        # Maybe we can use a chain and first we can return a response with a specific format like the persons, the date, the hour, etc. (we can have like a conversation)
        # and after we can use the response to create the meeting in the calendar that we have in the db.
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_improve_listening_template
        )
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_improve_listening_template
        )
        final_prompt = ChatPromptTemplate(
            messages=[system_message_prompt, human_message_prompt],
            input_variables=["output"],
            partial_variables={"format_instructions": format_instructions},
        )
        chain = LLMChain(llm=self._general_llm, prompt=final_prompt)
        overall_chain = SimpleSequentialChain(
            chains=[chain],
            verbose=True,
        )
        response = overall_chain.run(input)

        return output_parser.parse(response)
