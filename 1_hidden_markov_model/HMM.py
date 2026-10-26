from dataclasses import dataclass

import numpy as np
from itertools import product

@dataclass
class HMM:
    # initial probability, pi[i] = P(state i | start)
    # where i is the index of the state in states list
    pi: list[float]

    # transition probability, a[i,j] = P(state j | state i)
    a_ij: np.ndarray

    # observation likelihoods, b[i,o] = P(observation o | state i)
    # where o is the index of the observation in possible_observations
    b: np.ndarray
    states: list[any]
    possible_observations: list[any]

    def likelihood(self, observations: list[any]) -> float:
        """
        Compute the likelihood of a particular sequence of observations O

        There are two ways with N states and a seqence of length T: 
        - the naive method which is $$O(N^T)$$ in naive_likelihood
        - the forward algorithm which is $$O(N^2 T)$$ in forward_algorithm

        This calls the fast forward algorithm.

        Parameters:
        observations: a list of observations, likely strings, numbers, etc. converted to list of indices by the self.possible_observations object

        Returns:
        float of the likelihood, must be between 0 and 1. if you call the method for all possible observation sequences, the probability should sum to 1 (or near it cuz of rounding issues)
        """
        return self.forward_algorithm(observations)

    def forward_algorithm(self, observations: list[any]) -> float:
        # build P(O) iteratively using the forward algorithm $$O(N^2 T)$$

        # alpha is indexed as t, state, so # observations x # states
        alpha = np.zeros((len(observations), len(self.states))) # 
        # print(alpha)

        # find indices of the observations in the possible_observations table
        observation_indices = [self.possible_observations.index(o) for o in observations]
        # print(observations, observation_indices)

        # for each state, compute initial alphas for first step
        for j in range(len(self.states)):
            # get P(state | start) * P(first observation | state)
            alpha[0, j] = self.pi[j] * self.b[j, observation_indices[0]]

        # print(alpha[0, :])

        # then, for each step, add a new observation to each path

        # $$\alpha_t(j) = \sum_{i=1}^n \alpha_{t-1}(i) a_{ij} b_j(o_t)$$

        # $$\alpha_{t-1} (i)$$ is stored in alpha[t-1,i]

        # bad non-numpy method, but it works
        for t in range(1, len(observations)):
            for j in range(len(self.states)):
                # print(t, j, [np.round((alpha[t-1, i], self.a_ij[j, i], self.b[j, observation_indices[t]]), 5) for i in range(len(self.states))])
                alpha[t, j] = sum([(alpha[t-1, i] * self.a_ij[j, i] * self.b[j, observation_indices[t]]) for i in range(len(self.states))])

        # print(alpha)

        # use np.prod and np.sum across axes
        return np.sum(alpha[-1, :])


    def naive_likelihood(self, observations: list[any]):
        # for a given list of observations O,

        # $$P(O) = \sum_Q P(O,Q)$$ where Q are all of the possible hidden state sequences
        # this is $$O(N^T)$$

        p_o = 0

        # create every possible observations-long hidden state sequence
        Q = product(self.states, repeat=len(observations))
        
        # old version for just three-long observation
        # Q = [(i, j, k) for i in self.states for j in self.states for k in self.states]
        print(Q)

        for q in Q:
            # compute the likelihood for each state sequence, $$P(O,Q)$$
            p_o += self.compute_likelihood_given_state_sequence(observations, q)
        return p_o

    def compute_likelihood_given_state_sequence(self, observations, state_sequence):
        
        # compute $$P(O,Q) = P(O|Q) * P(Q) = \prod_i P(o_i | q_i) * \prod_i P(q_i | q_{i-1})$$

        # for example, P(313, hot hot cold) = P(hot|start) * P(hot|hot) * P(cold|hot)
        #                                   * P(3|hot) * P(1|hot) * P(3|cold)
        # which respectfully come from      = pi[1]        * a[1,1]    * a[0,1]
        #                                   * b[1]["3"]* b[1]["1"]* b[0]["3"]
        #                                   = .8           * .6         * .4
        #                                   * .4       * .2             * .1
        #                                   = 0.001536
        state_indices = [self.states.index(state) for state in state_sequence]

        # access pi[first_index]
        start = self.pi[state_indices[0]]
        prod = start
        # find $$P(o_i|q_i)$$ for each pair
        for i in range(len(state_sequence) - 1):
            # the pair is i and i + 1
            # probability of getting state i + 1 given state i
            prod *= self.a_ij[state_indices[i+1], state_indices[i]]

        # now get the b
        observation_indices = [self.possible_observations.index(o) for o in observations]
        for i in range(len(state_sequence)):
            prod *= self.b[state_indices[i], observation_indices[i]]

        # print(state_sequence, prod)
        return prod

def main():
    hmm = HMM(  
        pi = [.2, .8],
        a_ij=np.array([ [.5, .4],
                        [.5, .6],
                        ]),
        b = np.array([[.5, .4, .1],
                        [.2, .4, .4]]),
        states = ["Cold", "Hot"],
        possible_observations=[1,2,3]
    )
    # b is # state x # possible_observations

    p_o = hmm.naive_likelihood(observations = [3, 1, 3])
    print(p_o)

    # # testing that all possible observations add to 1
    # pos_obs = [(i, j, k) for i in hmm.possible_observations for j in hmm.possible_observations for k in hmm.possible_observations]
    # print("Should sum to 1:", sum([hmm.naive_likelihood(o) for o in pos_obs]))

    # agrees with naive method, nice!
    fast_likelihood = hmm.likelihood([3, 1, 3])
    print(fast_likelihood)

if __name__ == "__main__":
    main()
