from modules.listener.listener import Listener
from modules.roles.model_responses import MeetingResponse, Q_AResponse
from modules.roles.roles import FactoryRole


class ExecutionController:
    def __init__(self):
        self._listener = Listener()
        self._role_factory = FactoryRole()
        self._role_factory.reg_concrete_role("meeting", MeetingResponse())
        self._role_factory.reg_concrete_role("q_a", Q_AResponse())

    def _listen(self):
        return self._listener.execute()

    def execute(self):
        request = self._listen()
        role, requestEnhanced = self._role_factory.create_concrete_role(request)
        model_response = role.generate_response(requestEnhanced.req_text)
        print(model_response)
        # TODO: send model_response to the talker
