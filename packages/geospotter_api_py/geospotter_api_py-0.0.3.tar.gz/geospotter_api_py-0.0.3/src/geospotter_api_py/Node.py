class Node:
    def __init__(self, name:str, parent:"Node"=None, description:str=None) -> None:
        self.name = name
        self.parent = parent
        self.description = description
    
    def __repr__(self) -> str:
        tmp = f"name: {self.name}"
        if not self.parent is None:
            tmp += f", parent: {self.parent.name}"
        tmp+= f", descr: {self.description}"
        return tmp