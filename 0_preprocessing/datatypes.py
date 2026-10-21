from dataclasses import dataclass

@dataclass
class Node:
    node_id: str
    parent: "Node" | None
    children: list["Node"] | list[None]

    def add_child(self, child: Node):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

class Genome:
    def __init__(self, species_name):
        self.species = species_name
        self.nodes = {}
        self.root = Node(species_name, None)

    def add_node(self, child: Node, parent: Node):
        parent.add_child(child)
        self.nodes[child.node_id] = child

    def get_node(self, node_id):
        return self.nodes.get(node_id)

class Chromosome(Node):
    def __init__(self, chromo_id: str, species_id: str, length: int):
        super().__init__(chromo_id, species_id)
        self.length = length

class Gene(Node):
    def __init__(self, species_name, chromosome):
        super().__init__(species_name, chromosome)
        self.start: int
        self.end: int
        self.strand: bool
        self.family: str
