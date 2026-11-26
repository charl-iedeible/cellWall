from multiprocessing import Pool
import time

from datatypes import Genome

def run_tests(test: str, file_tuple: (str, str)) -> Genome, process_time:
    start_time = time.time()
    
    if test == 'hmmrXblast':
        pass
    elif test == 'hmmrXlite':
        pass
    elif test == 'cheaterXblast':
        pass
    elif test == 'cheaterXlite':
        pass
    else:
        print('Girl what?')

    return genome_analysis, start_time - time.time()

def multi_process_test(tests_to_run: [tuple(str, str)]) -> [Node()]:
    with Pool() as pool:
        results = pool.starmap(tests_to_run, run_tests)
    # organize each result into a corresponding node per analysis method and return

# set working directory. There should be a folder of analysis_species containing folders with each species abbreviation. In those folders should be a GFF3 structure file and a DNA-seq FASTA

# cycle through each species in the folder, create a tuple of GFF3 filepath then FASTA file path for each species

# extract ref_dict pickles (HMMR and cheater HMMR)

# for each species, run four analyses (factorialization across ref_dicts and HMMR methods) using multiprocessing to reduce runtimes
tests_to_run = []
test_pool = ['hmmrXblast', 'hmmrXlite', 'cheaterXblast', 'cheaterXlite']

for file_tuple in file_tuples:
    for test in test_pool:
        tests_to_run.append((test, file_tuple))

result_tree = multi_process_test(tests_to_run)



# save results

# run syteny analysis?