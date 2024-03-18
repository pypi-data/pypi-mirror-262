class Node:
    def __init__(self, name:str, parent:"Node"=None) -> None:
        self.name = name
        self.parent = parent