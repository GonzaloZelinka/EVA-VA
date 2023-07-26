from langchain.output_parsers import ResponseSchema


req_text = ResponseSchema(
    name="req_text",
    description="The string improved and translated into English",
)

req_type = ResponseSchema(
    name="req_type",
    description="The type of request \
        generated for the LLM. the possible values are: \
          meeting and q_a",
)

response_schemas = [req_text, req_type]
