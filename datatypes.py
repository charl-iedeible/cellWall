from dataclasses import dataclass, field

@dataclass
class Node:
    node_id: str
    parent: "Node" | "None" = None
    children: list["Node"] | list = field(default_factory=list)

    def add_child(self, child: "Node"):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

class Genome:
    def __init__(self, species_name):
        self.species = species_name
        self.nodes = {}
        self.root = Node(node_id=species_name, parent=None)

    def add_node(self, child: Node, parent: Node):
        parent.add_child(child)
        self.nodes[child.node_id] = child

    def get_node(self, node_id):
        return self.nodes.get(node_id)

class Chromosome(Node):
    def __init__(self, chromo_id: str, genome: Node, length: int):
        super().__init__(node_id=chromo_id, parent=genome)
        self.length = length

class Gene(Node):
    def __init__(self, gene_id: str, chromosome: Node):
        super().__init__(node_id=gene_id, parent=chromosome)
        self.start: int = 0
        self.end: int = 0
        self.strand: bool | None = None
        self.family: str | None = None
        
class EvolutionaryTree:
    def __init__(self, name):
        self.name = name
        self.nodes = {}
        self.root = Species | None = None
        
    def add_node(self, child: Node, parent: Node):
        parent.add_child(child)
        self.nodes[child.node_id] = child

    def get_node(self, node_id):
        return self.nodes.get(node_id)

class Species(Node):
    def __init__(self, species_name: str, parent: Node):
        super().__init__(node_id=species_name, parent=parent)
        self.genome = Genome | None = None
        self.lineage: str | None = None
        self.color: str | None = None
