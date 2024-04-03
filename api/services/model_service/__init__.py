from api.config import Config
from api.services.google_firestore_service.repositories.error import create_error
from api.services.model_service.roles.chains_creator import (
    ChainQ_ACreator,
    ChainToDoCreator,
    FactoryChain,
)
from langchain.chat_models import ChatOpenAI

from api.utils.database_error import ToDatabaseException


class ModelService:

    def __init__(self):
        print("\033[96mLoading Model Service..\033[0m", end="")
        self.__chain_factory = FactoryChain()
        self.__llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")
        self.__chain_factory.reg_concrete_chain("q_a", ChainQ_ACreator())
        self.__chain_factory.reg_concrete_chain("todo", ChainToDoCreator())
        print("\033[90m Model Service load complete.\033[0m\n")

    def execute(self, request):
        request_enhanced = {"req_text": None, "req_type": None}
        try:
            chain_creator, request_enhanced = (
                self.__chain_factory.create_concrete_chain_creator(request, self.__llm)
            )
            response = chain_creator.execute(request_enhanced["req_text"], self.__llm)

            return response
        except ToDatabaseException as e:
            initial_error = e.to_dict()
            error = {
                **initial_error,
                "initialRequestText": request_enhanced["req_text"],
                "initialRequestType": request_enhanced["req_type"],
            }
            create_error(error)
            return "An error occurred, please try again later, the error has been added correctly to the database."
        except Exception as e:
            print("MODEL SERVICE ERROR ", e)
            error = {
                "message": str(e),
                "details": "An error occurred, please try again later.",
                "code": 500,
                "createdBy": Config.USER_ID,
                "initialRequestText": request_enhanced["req_text"],
                "initialRequestType": request_enhanced["req_type"],
            }
            create_error(error)
            return "An unexpected error occurred, not catched by ToDatabaseException, the error has been added correctly to the database."
