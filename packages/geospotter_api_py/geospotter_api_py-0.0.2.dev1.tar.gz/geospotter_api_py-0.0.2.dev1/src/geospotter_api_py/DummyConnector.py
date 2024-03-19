from .Node import Node

"""
This is a class made to emulate the API without a real server running
"""

class DummyConnector():
    nodes = []

    def __init__(self) -> None:
        camerino = Node("Camerino", description="Descrizione di Camerino")
        self.nodes.append(camerino)
        self.nodes.append(Node("Rocca Varano", camerino, "Castello molto bello"))

        castelraimondo = Node("Castlelraimondo",description="Descrizione di Castelraimondo")
        self.nodes.append(castelraimondo)
        self.nodes.append(Node("Porchettaro", castelraimondo, "Panini buoni a ottimi prezzi. Ben fornito di diverse carni e formaggi."))
        self.nodes.append(Node("Stazione Trenitalia", castelraimondo, "Ciuuu ciuuu!!"))

    def GetAllNodes(self)->list[Node]:
        return self.nodes
    
    def SearchNodes(self, query)->list[Node]:
        res = []
        for node in self.GetAllNodes():
            if query in node.name:
                res.append(node)
        return res