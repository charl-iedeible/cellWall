
from dataclasses import dataclass, field


@dataclass
class Node:
    """
    Divyata Bhatt & Charlie Deible, debugged with ChatGPT
    Base class for all nodes in the genome hierarchy.
    """

    node_id: str
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)

    def add_child(self, child: "Node") -> None:
        """Add a child and establish its parent relationship."""

        if child.parent is not None and child.parent is not self:
            raise ValueError(
                f"{child.node_id} already belongs to another parent."
            )

        if child not in self.children:
            self.children.append(child)

        child.parent = self

    def get_children(self) -> list["Node"]:
        return self.children

    def get_parent(self) -> "Node | None":
        return self.parent


class Genome:
    """
    Divyata Bhatt & Charlie Deible, debugged with ChatGPT
    Root object containing chromosomes and their genes.
    """

    def __init__(self, species_name: str):
        self.species = species_name
        self.root = Node(node_id=species_name)

        # Centralized lookup of all nodes by ID.
        self.nodes: dict[str, Node] = {}

    def add_node(self, child: Node, parent: Node) -> None:
        """Add a node to the hierarchy and register it."""

        if child.node_id in self.nodes:
            raise ValueError(
                f"Duplicate node ID: {child.node_id}"
            )

        if parent is not self.root and parent.node_id not in self.nodes:
            raise ValueError(
                f"Parent {parent.node_id} is not registered."
            )

        parent.add_child(child)
        self.nodes[child.node_id] = child

    def get_node(self, node_id: str) -> Node | None:
        return self.nodes.get(node_id)

    def get_chromosomes(self) -> list["Chromosome"]:
        return [
            node for node in self.root.children
            if isinstance(node, Chromosome)
        ]


class Chromosome(Node):
    """
    Divyata Bhatt & Charlie Deible, debugged with ChatGPT
    Chromosome node belonging to a genome.
    """

    def __init__(
        self,
        chromo_id: str,
        genome: Node,
        length: int | None = None
    ):
        super().__init__(
            node_id=chromo_id,
            parent=genome
        )

        self.length = length


class Gene(Node):
    """
    Divyata Bhatt & Charlie Deible, debugged with ChatGPT
    Gene node belonging to a chromosome.
    """

    def __init__(
        self,
        gene_id: str,
        chromosome: Node,
        start: int,
        end: int,
        strand: str,
        biotype: str | None = None,
        name: str | None = None,
        arth_match: str | None = None
    ):
        super().__init__(
            node_id=gene_id,
            parent=chromosome
        )

        self.start = start
        self.end = end
        self.strand = strand

        self.biotype = biotype
        self.name = name

        # Arabidopsis reference gene with the closest 3-mer match.
        self.arth_match = arth_match

    @property
    def length(self) -> int:
        """GFF3 coordinates are 1-based and inclusive."""
        return self.end - self.start + 1

class Analysis(Node):
    """
    Charlie Deible
    Root Nodes for each of the analysis methods to make pickle storage and reuse more streamline.
    """
    def __init__(self, method: str):
        super().__init__(node_id=method)
        self.run_time: dict[str, float] = {}   # keep track of how long each analysis took

    # edit add_child() to keep track of time analysis took in dictionary
    def add_genome(self, child: Genome, time: float) -> None:
        self.children.append(child)
        self.run_time[child.species] = time
