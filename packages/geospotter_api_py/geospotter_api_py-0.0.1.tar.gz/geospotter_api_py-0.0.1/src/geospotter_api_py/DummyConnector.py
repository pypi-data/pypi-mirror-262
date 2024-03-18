from .Node import Node

class DummyConnector():
    nodes = []

    def __init__(self) -> None:
        camerino = Node("Camerino")
        self.nodes.append(camerino)
        self.nodes.append(Node("Rocca Varano", camerino))

        castelraimondo = Node("Castlelraimondo")
        self.nodes.append(castelraimondo)
        self.nodes.append(Node("Porchettaro", castelraimondo))
        self.nodes.append(Node("Stazione Trenitalia", castelraimondo))

    def GetAllNodes(self)->list[Node]:
        return self.nodes