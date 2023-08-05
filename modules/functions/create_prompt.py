from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from typing import List, Mapping


def create_prompt(
    system_prompt: SystemMessagePromptTemplate,
    human_prompt: HumanMessagePromptTemplate,
    input_variables: List[str],
    # partial_variables: Mapping[str, str],
) -> ChatPromptTemplate:
    final_system_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
    final_human_prompt = HumanMessagePromptTemplate.from_template(human_prompt)
    final_prompt = ChatPromptTemplate(
        messages=[final_system_prompt, final_human_prompt],
        input_variables=input_variables,
        # partial_variables=partial_variables,
    )
    return final_prompt
