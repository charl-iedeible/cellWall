from dataclasses import dataclass

import numpy as np

@dataclass
class HMM:
    pi: list[float]
    a_ij: np.ndarray
    b: np.ndarray
    states: list[any]
    possible_observations: list[any]

    def naive_likelihood(self, observations: list[any]):
        # for a given list of observations O,

        # $$P(O) = \sum_Q P(O,Q)$$ where Q are all of the possible hidden state sequences

        p_o = 0

        # create every possible three-long hidden state sequence
        # TODO: make this happen for all possible lengths (possibly cartesian product?)
        Q = [(i, j, k) for i in self.states for j in self.states for k in self.states]
        print(Q)

        for q in Q:
            # compute the likelihood for each state sequence, $$P(O,Q)$$
            p_o += self.compute_likelihood_given_state_sequence(observations, q)
        return p_o

    def compute_likelihood_given_state_sequence(self, observations, state_sequence):
        # compute $$P(O,Q) = P(O|Q) * P(Q) = \prod_i P(o_i | q_i) * \prod_i P(q_i | q_{i-1})$$

        # for example, P(313, hot hot cold) = P(hot|start) * P(hot|hot) * P(cold|hot)
        #                                   * P(3|hot) * P(1|hot) * P(3|cold)
        # which respectfully come from      = pi[1]        * a[1][1]    * a[0][1]
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
            prod *= self.a_ij[state_indices[i], state_indices[i+1]]

        # now get the b
        observation_indices = [self.possible_observations.index(o) for o in observations]
        for i in range(len(state_sequence)):
            prod *= self.b[state_indices[i], observation_indices[i]]

        print(state_sequence, prod)
        return prod

def main():
    hmm = HMM(  
        pi = [.2, .8],
        a_ij=np.array([ [.5, .5],
                        [.6, .4],
                        ]),
        b = np.array([[.5, .4, .1],
                        [.2, .4, .4]]),
        states = ["Cold", "Hot"],
        possible_observations=[1,2,3]
    )

    p_o = hmm.naive_likelihood(observations = [3, 1, 3])
    print(p_o)

    # testing that all possible observations add to 1
    pos_obs = [(i, j, k) for i in hmm.possible_observations for j in hmm.possible_observations for k in hmm.possible_observations]
    print("Should sum to 1:", sum([hmm.naive_likelihood(o) for o in pos_obs]))

if __name__ == "__main__":
    main()
