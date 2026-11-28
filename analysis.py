from multiprocessing import Pool
import time
import os

from datatypes import Genome, Analysis
from functions import initialize_GFF3

test_pool = ['hmmrXblast', 'hmmrXlite', 'cheaterXblast', 'cheaterXlite']

def run_tests(args: tuple) -> tuple[Genome, float, str]:
    """
    Charlie Deible
    This is a wrapper function to manage the pool of workers running different test types.
    Runs the proper test and keeps track of how long it took.
    """
    test, file_tuple = args
    start_time = time.time()
    
    if test == 'hmmrXblast':
        pass
    elif test == 'hmmrXlite':
        genome_analysis = initialize_GFF3(file_tuple[0], file_tuple[1], get_hmmr_pickle(), 10, 5)
    elif test == 'cheaterXblast':
        pass
    elif test == 'cheaterXlite':
        genome_analysis = initialize_GFF3(file_tuple[0], file_tuple[1], get_the_pickle_that_cheats(), 10, 5)
    else:
        print('Girl what?')

    return genome_analysis, time.time() - start_time, test

def multi_process_test(tests_to_run: [tuple(str, str)]) -> [Node()]:
    """
    Charlie Deible
    Run the different tests at the same time.
    """
    analysis_tree = {
        'hmmrXblast':Analysis('hmmrXblast'),
        'hmmrXlite':Analysis('hmmrXlite'),
        'cheaterXblast':Analysis('cheaterXblast'),
        'cheaterXlite':Analysis('cheaterXlite')
    }
    
    with Pool() as pool:
        results = pool.imap_unordered(run_tests, tests_to_run)
        
        # organize each result into a corresponding node per analysis method and return
        for result in results:
            analysis_tree[result[2]].add_genome(result[0], result[1])
            print(f"Analysis of {result[0].species} with {result[2]} has been processed.")
            print(f"Tha analysis took {result[1]} seconds.")

    return analysis_tree

def get_file_tuples() -> list(tuple()):
    """
    Charlie Deible
    Cycle through 'inputs' folder and initialize tuple pairs of folders necessary for the DNA analysis.
    """
    parent_folder = os.getcwd() + '/inputs'
    file_pairs = []
    
    for root, dirs, files in os.walk(parent_folder):
        if root == parent_folder:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            if '.gff3' in file:
                gff3_file = file_path
            elif 'cdna' in file:
                fasta_file = file_path
    
        file_pairs.append((gff3_file, fasta_file))
    return file_pairs

def get_hmmr_pickle() -> dict():
    return os.getcwd() + pickle_address

def get_the_pickle_that_cheats() -> dict():
    return os.getcwd() + cheater_pickle_address

def main():
    """
    Charlie Deible
    Main function that implements all of the other functions to actually run the factorial analyses.
    """
    # for each species, run four analyses (factorialization across ref_dicts and HMMR methods) using multiprocessing to reduce runtimes
    tests_to_run = []
    
    for file_tuple in get_file_tuples():
        for test in test_pool:
            tests_to_run.append((test, file_tuple))
    
    result_tree = multi_process_test(tests_to_run)

    # save results
    pickle_address = '/outputs/analysis' + str(int(time.time())) + '.pkl'
    with open(pickle_address, "wb") as f:
        pickle.dump(result_tree, f)

main()
