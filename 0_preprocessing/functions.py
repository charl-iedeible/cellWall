

# define genome from GFF3
def initialize_GFF3(str: file) -> Genome:
    # initialize a genome object to append appropriate line data to
    genome = Genome(species=)

    searching = True
    initializing = False
    adding = False
    # line by line, determine if we are searching for parent, initializing parent, or adding nodes
    for line in file:
        while searching:
            # check if beginning of new parent ('###')
            if line.rstrip() == '###':
                searching = False
                initializing = True
                continue

        while initializing:
            if line[0] == '#':
                continue
            fields = line.rstrip().split("\t")  # split tab string into fields
            attributes = parse_attributes(fields[8])    # get dictionary of attributes
            # check if a gene or new chomosome
            if attributes["ID"][:4] == 'gene':
                # check if gene is a cell wall gene, skip rest
                if is_cell_wall(attributes["ID"]):
                    initializing = False
                    adding = True
                    pass # initialize gene object and append to chromosome object
                else:
                    initializing = False
                    searching = True
            elif attributes["ID"][:6] == 'region':
                # initialize chromosome and append to genome object
                chromo_num = int(attributes["ID"][7:])
                chromo_len = int(fields[5])
                current_chromo = Chromosome(chromo_num, genome.species, chromo_len)
                genome.add_node(current_chromo, genome.species)
                # stay in initializing phase to add genes
                

        while adding:
            if line[0] == '#':
                adding = False
                initializing = True
                continue
            fields = line.rstrip().split("\t")  # split tab string into fields
            attributes = parse_attributes(fields[8])    # get dictionary of attributes            
        


# parse attributes of line
def parse_attributes(str: attributes) -> dict:
    pairs = {}
    # split lines by semi-colon, then equal sign
    for pair in attributes.split(';'):
        for key, value in pair.split('='):
            pairs[key] = value
    return pairs
