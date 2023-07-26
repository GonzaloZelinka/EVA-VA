from abc import ABC, abstractmethod


class ModelResponse(ABC):
    @abstractmethod
    def process_req(self):
        pass


class MeetingResponse(ModelResponse):
    def __init__(self):
        pass

    def process_req(self):
        return "MeetingResponse"


class Q_AResponse(ModelResponse):
    def __init__(self):
        pass

    def process_req(self):
        return "Q_AResponse"
