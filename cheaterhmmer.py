import pyhmmer
import os
import pandas as pd
import pickle
from pathlib import Path

def big_boy_hmmscan():
    # make intermediates folder
    Path("intermediates").mkdir(exist_ok=True)
    
    genome_folders = [x for x in os.listdir("inputs/") if os.path.isdir("inputs/"+x)]
    
    for genome in genome_folders:
        peptide_fasta = f"inputs/{genome}/{genome}_pep.fa"
        
        # using the fasta file, perform a scan over all HMM models
        # to match peptides in the target genomes to arabidopsis cell wall protein families

        # should be digital as described here https://pyhmmer.readthedocs.io/en/latest/examples/active_site.html#Loading-digitized-sequences
        with pyhmmer.easel.SequenceFile(peptide_fasta, digital=True) as sequences:
            
            with pyhmmer.plan7.HMMPressedFile("hmms/pressed") as hmm_db:                
                hits_by_sequence = list(pyhmmer.hmmer.hmmscan(sequences, hmm_db))

            with open(f"intermediates/{genome}_hits_by_sequence.pkl", "wb+") as f:
                 pickle.dump(hits_by_sequence, f)

        # results in list of lists of "Hit" objects
        print(genome, "number of hits:", sum([len(list(hits)) for hits in hits_by_sequence]))

if __name__ == "__main__":

    # only need to run once, writes to intermediates/{genome}_hits_by_sequence.pkl files
    big_boy_hmmscan()
    
    