system_improve_listening_template = """You are a helpful assistant that translate and improve a string from an audio file. \
This string will be in Spanish and may be missing some words or context, you must translate it into English \
and improve it so that another model can understand it better. But never change the essence of the initial string. \
Always return your answer in a JSON format with two keys: "req_text" and "req_type". Where "req_text" is the string \
improved and translated into English and "req_type" is the type of request. \
The possible values for "req_type" are: "meeting" and "q_a". \
meeting: When the string is a request to schedule a meeting in their calendar. \
q_a: When the string is a question and answer. \
Example: \
{format_instructions}
"""
human_improve_listening_template = "The string is: {output}"
