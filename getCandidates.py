"""
    Charlie Deible
    functions associated with testing if a given nucleotide sequence is one of interest
"""
from collections import Counter
import pickle

def get_3mer_dict(seq: str) -> dict:
    """
        turn a nucleotide sequence into a dictionary of 3-mers and occurences
    """
    tmer_dict = {}

    # cycle through 3 char string windows
    for i in range(3, len(seq)):
        tmer = seq[i - 3:i]
        tmer_dict[tmer] = tmer_dict.get(tmer, 0) + 1   # append to dictionary

    return tmer_dict

def initialize_3mer_dict():
    """
        initialize a reference dictionary with all possible 3-mers as keys with empty dictionaries as the value
    """
    bases = "ATCG"
    tmer_dict = {}

    for mer in product(bases, repeat=3):
        tmer = "".join(mer)
        tmer_dict[tmer] = {}

    return tmer_dict

def add_gene_to_ref(ref_dict: dict, gene_dict: dict, name: str) -> dict:
    """
        incorporate a 3-mer dict of a nucleotide sequence into the reference dictionary
    """
    for tmer in gene_dict.keys():
        ref_dict[tmer].setdefault(gene_dict[tmer], []).append(name)
    
    return ref_dict

def find_matches(ref_dict: dict, gene_dict: dict, tmer_bound: int, match_bound: int) -> list:
    """
        compare a given nucleotide sequence's 3-mer dictionary to sequences in the reference dictionary
        return a list of genes in the reference dictionary with the closest matches
    """
    match_list = []

    # cycle through all possible 3-mers (included in the reference dictionary)
    for tmer in ref_dict.keys():
        if gene_dict.get(tmer):   # make sure 3-mer is in the query sequence
            # cycle through reference genes that have occurences of that 3-mer within the range allowed by tmer_bound input
            for num_tmer in range(max(0, gene_dict[tmer] - tmer_bound // 2),   # return 0 if lower range goes into the negatives
                                  (gene_dict[tmer] + tmer_bound // 2) + 1):
                match = ref_dict[tmer].get(num_tmer)   # get list of reference genes that match
                if match:
                    match_list += match   # concatenate elements to the larger match list

    matches = []
    counts = Counter(match_list)   # returns dictionary with gene name as the key and occurences in the match list as the value, sorted in decreasing order of values

    # cycle through genes with matches within the match bound
    for gene, num_match in counts.items():
        if num_match in range(len(gene_dict.keys()) - match_bound, len(gene_dict.keys()) + 1):
            matches.append(gene)
        else:
            break
    
    return matches

def is_interest(querey_seq: str, ref_dict: dict, tmer_bound: int, match_bound: int) -> bool:
    """
        determine if a querey seq is potentially a gene worth downstream blast analysis given its how close it is to a set of reference genes
    """
    if find_matches(ref_dict, get_3mer_dict(querey_seq), tmer_bound, match_bound):
        return True
    return False

