from .DummyConnector import DummyConnector
from .Node import Node

class GeoSpotterApi():
    def __init__(self, useDummyConnector:bool = False) -> None:
        if useDummyConnector:
            self.api = DummyConnector()
        else:
            raise Exception("Real connector not implemented, use dummy")
    
    def GetAllNodes(self)->list[Node]:
        return self.api.GetAllNodes()