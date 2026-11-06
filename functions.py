from datatypes import Node, Genome, Chromosome, Gene
from Bio import SeqIO

# define genome from GFF3
def initialize_GFF3(filename_GFF3: str, filename_FASTA: str, cell_wall_genes:list[str], tmer_bound: int, match_bound: int) -> Genome:
    # turn FASTA into dictionary

    genome = SeqIO.to_dict(SeqIO.parse(filename_FASTA, "fasta"))
    
    # initialize a genome object to append appropriate line data to
    
    species_name = filename.split("/")[-1].split("_gca")[0]
    genome = Genome(species_name=species_name)

    searching = True
    initializing = False
    adding = False

    # line by line, determine if we are searching for parent, initializing parent, or adding nodes

    with open(filename) as file:
        for line in file:
            line = line.rstrip()

            if searching:
                # check if beginning of new parent ('###')
                if line == '###':
                    searching = False
                    initializing = True
                    continue
                if line[0] != '#':
                    fields = line.split('\t')
                    attributes = parse_attributes(fields[8])
                    gene_id = attributes.get('ID', '')
                    if gene_id[:6] == 'region':
                        chromo_id = gene_id.split(':')[1]
                        chromo_len = int(fields[4]) - int(fields[3])
                        current_chromo = Chromosome(chromo_id, genome.root, chromo_len)
                        genome.add_node(current_chromo, genome.root)
                
            elif initializing:
                if line[0] == '#':
                    continue
                fields = line.split("\t")  # split tab string into fields
                attributes = parse_attributes(fields[8])    # get dictionary of attributes
                # check if a gene or new chomosome
                gene_id = attributes.get("ID", "")
                if gene_id[:4] == 'gene':
                    if is_interest(genome[gene_id], cell_wall_genes, tmer_bound, match_bound):
                    # check if gene is a cell wall gene, skip rest
                        initializing = False
                        adding = True
                        # initialize gene object and append to chromosome object
                        gene_id = gene_id.split(":")[1]
                        current_gene = Gene(gene_id, current_chromo)
                        genome.add_node(current_gene, current_chromo)

                    else:
                        initializing = False
                        searching = True
                elif gene_id[:6] == 'region':
                    # initialize chromosome and append to genome object
                    chromo_id = gene_id.split(":")[1]
                    chromo_len = int(fields[4]) - int(fields[3])
                    current_chromo = Chromosome(chromo_id, genome.root, chromo_len)
                    genome.add_node(current_chromo, genome.root)
                    # stay in initializing phase to add genes

            elif adding:
                if line[0] == '#':
                    adding = False
                    initializing = True
                    continue
                fields = line.split("\t")  # split tab string into fields
                attributes = parse_attributes(fields[8])    # get dictionary of attributes  
    return genome          

# parse attributes of line
def parse_attributes(attributes: str) -> dict:
    pairs = {}
    # split lines by semi-colon, then equal sign
    for pair in attributes.split(';'):
        if '=' in pair:
            key, value = pair.split('=',1)
            pairs[key] = value
    return pairs

if __name__ == "__main__":
    genome = initialize_GFF3("achillea_ptarmica_gca982375345v1.gff3 2", [])
    print(genome.root.node_id)
    print(genome.nodes.keys())
    print("Species:", genome.root.node_id)
    print("Chromosomes:", [n for n in genome.nodes if len(n) < 10])
    print("Gene count:", len([n for n in genome.nodes if len(n) > 10]))
