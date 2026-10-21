from datatypes import Node, Genome, Chromosome, Gene

# define genome from GFF3
def initialize_GFF3(filename: str, cell_wall_genes:list[str]) -> Genome:
    # initialize a genome object to append appropriate line data to
    genome = Genome(species_name=filename)

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

            elif initializing:
                if line[0] == '#':
                    continue
                fields = line.split("\t")  # split tab string into fields
                attributes = parse_attributes(fields[8])    # get dictionary of attributes
                # check if a gene or new chomosome
                if attributes["ID"][:4] == 'gene':
                    # check if gene is a cell wall gene, skip rest
                    if in_cell_wall(attributes["ID"], cell_wall_genes):
                        initializing = False
                        adding = True
                        # initialize gene object and append to chromosome object
                        gene_id = attributes["ID"].split(":")[1]
                        current_gene = Gene(gene_id, current_chromo.node_id)
                        genome.add_node(current_gene, current_chromo)

                    else:
                        initializing = False
                        searching = True
                elif attributes["ID"][:6] == 'region':
                    # initialize chromosome and append to genome object
                    chromo_id= attributes["ID"].split(":")[1]
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


# parse attributes of line
def parse_attributes(attributes: str) -> dict:
    pairs = {}
    # split lines by semi-colon, then equal sign
    for pair in attributes.split(';'):
        if '=' in pair:
            key, value = pair.split('=',1)
            pairs[key] = value
    return pairs


#read file containting cell wall protein data and turn it into a list of genes corresponding to proteins


def in_cell_wall(gene:str, cell_wall_genes:list[str]) -> bool:
    for g in cell_wall_genes:
        if g == gene:
            return True
    return False
