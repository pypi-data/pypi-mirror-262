class Node:
    def __init__(self, name:str, parent:"Node"=None, description:str=None) -> None:
        self.name = name
        self.parent = parent
        self.description = description