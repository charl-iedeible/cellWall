from dataclasses import Genome, Chromosome, Gene

#pairwise alignment

def compare_genomes(genome_1: Genome, genome_2: Genome, threshold: float) -> list[tuple]:
    synteny_pair = []
    for gene_i in genome_1:
        for gene_j in genome_2:
            if gene_i.sequence is None or gene_j.sequence is None:
                continue
            similarity_score = align_genes(gene_i.sequence, gene_j.sequence)
            if similarity_score > threshold:
                synteny_pair.append((gene_i,gene_j))
    return synteny_pair

def align_genes(gene_1: str, gene_2: str) -> int:
    count_matches = 0
    len_shorter = min(len(gene_1),len(gene_2))
    for i in range(len_shorter):
        if gene_1[i] == gene_2[i]:
                count_matches += 1
    return count_matches/len_shorter
#use Biopython pairwise2

def synteny(database: Tree, arabidopsis_genome: Genome, threshold) -> dict:
    gene_dict = {gene.id: [] for gene in arabidopsis_genome}
    for random_genome in database:
        pairs = compare_genomes(arabidopsis_genome, random_genome,threshold)
        for a_gene, random_gene in pairs:
            gene_dict[a_gene.id].append(random_gene)
    return gene_dict
