from modules.listener.listener import Listener
from modules.roles.chains_creator import (
    FactoryChain,
    ChainMeetingCreator,
    ChainQ_ACreator,
)


class ExecutionController:
    def __init__(self):
        # self._listener = Listener()
        self.__chain_factory = FactoryChain()
        self.__chain_factory.reg_concrete_chain("meeting", ChainMeetingCreator())
        self.__chain_factory.reg_concrete_chain("q_a", ChainQ_ACreator())

    def _listen(self):
        return self._listener.execute()

    def execute(self, request):
        # request = self._listen()
        (
            chain_creator,
            requestEnhanced,
        ) = self.__chain_factory.create_concrete_chain_creator(request)
        print(requestEnhanced)
        response = chain_creator.execute(requestEnhanced["req_text"])
        print(response)
