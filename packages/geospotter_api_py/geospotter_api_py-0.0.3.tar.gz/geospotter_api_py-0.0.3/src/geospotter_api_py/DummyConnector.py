from .Node import Node

"""
This is a class made to emulate the API without a real server running
"""

class DummyConnector():

    def __init__(self) -> None:
        self.nodes = []
        camerino = Node("Camerino", description="Descrizione di Camerino")
        self.nodes.append(camerino)
        self.nodes.append(Node("Rocca Varano", camerino, "Castello molto bello"))

        castelraimondo = Node("Castelraimondo",description="Descrizione di Castelraimondo")
        self.nodes.append(castelraimondo)
        self.nodes.append(Node("Porchettaro", castelraimondo, "Panini buoni a ottimi prezzi. Ben fornito di diverse carni e formaggi."))
        self.nodes.append(Node("Stazione Trenitalia", castelraimondo, "Ciuuu ciuuu!!"))

    def GetAllNodes(self)->list[Node]:
        return self.nodes
    
    def SearchNodes(self, query:str)->list[Node]:
        query = query.lower()
        res = []
        for node in self.GetAllNodes():
            if query in node.name.lower():
                res.append(node)
            elif node.parent is None:
                continue
            elif query in node.parent.name.lower():
                res.append(node)
                
        return res