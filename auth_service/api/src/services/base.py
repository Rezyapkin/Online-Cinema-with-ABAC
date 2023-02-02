from abc import ABC, abstractmethod

from grpc import Channel as GrpcChannel


class BaseService(ABC):
    def __init__(self, grpc_channel: GrpcChannel):
        self.channel = grpc_channel
        self.stub = self.get_stub()

    @abstractmethod
    def get_stub(self):
        raise NotImplementedError()
