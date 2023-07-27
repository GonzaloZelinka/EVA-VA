from modules.listener.listener import Listener
from modules.roles.roles import FactoryRole, MeetingCreator, Q_ACreator


class ExecutionController:
    def __init__(self):
        # self._listener = Listener()
        self._role_factory = FactoryRole()
        self._role_factory.reg_concrete_role("meeting", MeetingCreator())
        self._role_factory.reg_concrete_role("q_a", Q_ACreator())

    def _listen(self):
        return self._listener.execute()

    def execute(self):
        request = self._listen()
        role, requestEnhanced = self._role_factory.create_concrete_role(request)
        # model_response = role.generate_response(requestEnhanced.req_text)
        # print(model_response)
        # TODO: send model_response to the talker

    def testing(self, text):
        role, requestEnhanced = self._role_factory.create_concrete_role(text)
        model_response = role.factory_model_response().process_req()
        print(model_response, requestEnhanced)
