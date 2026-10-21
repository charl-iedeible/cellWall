import pytest
from pathlib import Path
import math
import numpy as np

from HMM import HMM

def read_file(file_path:Path) -> list:
    l = list()
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            l.extend(line.rstrip("\n").split(" "))
    return [float(x) for x in l if x != ''] # convert everything to a float

def read_file_separated(file_path:Path) -> list[list[float]]:
    l = list()
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#") or line == '':
                continue
            listified = [float(x) for x in line.rstrip("\n").split(" ") if x != '']
            if len(listified) > 0:
                l.append(listified) 
    return l # list of lists where each list is a line in the output file

def read_hmm_test(file_path:Path) -> tuple[HMM, list[list]]:
    """
    Reads in an HMM test

    Returns:
    - HMM object to perform a test on 
    - list of lists of parameters to input into a function
    """
    l: list[list] = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#") or line == '':
                continue
            listified = [str(x) for x in line.rstrip("\n").split(" ") if x != '']
            if len(listified) > 0:
                l.append(listified) 
    # first after comments are states, then possible_observations, 
    # then a_ij (whose size depends on the length of states),
    # then b (whose size depends on lenght of states AND possible_observations)
    # then pi
    states = l[0]
    possible_observations = l[1]

    # a are all lists from 2 to 2 + the number of states + 1
    a_ij = np.array(l[2:2+len(states)], dtype=np.float32)

    # b are all lists starting from th end of a + the number of states + 1
    b = np.array(l[2+len(states): 2+len(states) + len(states)], dtype=np.float32)

    # pi is the next list
    pi = [float(x) for x in l[2+len(states) + len(states)]]

    hmm = HMM(pi, a_ij, b, states, possible_observations)

    # the test parameters are all the lists after that
    test_parameters = l[2+len(states) + len(states) + 1:]

    return (hmm, test_parameters)

def get_test_cases(test_name):
    # function written by ChatGPT
    input_path = Path("tests") / test_name / "input"
    return range(len(list(input_path.glob("input_*.txt"))))

# parametrization written by ChatGPT (nothing else though)
@pytest.mark.parametrize("i", get_test_cases("compute_likelihood_given_state_sequence"))
def test_compute_likelihood_given_state_sequence(i):
    # read in the inputs and the truth value
    test_path = Path("tests/compute_likelihood_given_state_sequence")
    hmm, params = read_hmm_test(test_path / "input" / f"input_{i}.txt")
    truth = read_file(test_path / "output" / f"output_{i}.txt")

    # compute our output
    observations, state_sequences = params
    output = [hmm.compute_likelihood_given_state_sequence(observations, state_sequences)]

    # check the computed values and actual values are close to equal
    assert output == pytest.approx(truth, rel=1e-6)

# @pytest.mark.parametrize("i", get_test_cases("naive_likelihood"))
# def test_naive_likelihood(i):
#     test_path = Path("tests/naive_likelihood")
#     inputs = read_file_separated(test_path / "input" / f"input_{i}.txt")
#     truth = read_file(test_path / "output" / f"output_{i}.txt")

#     first = OrderedPair(inputs[0], inputs[1])
#     second = OrderedPair(inputs[2], inputs[3])
#     raw_out = first + second
#     output = [raw_out.x, raw_out.y]

#     assert output == pytest.approx(truth, rel=1e-2)