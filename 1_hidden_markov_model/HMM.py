import numpy as np
from itertools import product
import graphviz

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

    alpha: np.ndarray
    beta: np.ndarray

    def __init__(self, pi: list[float], a_ij: np.ndarray, b: np.ndarray, states: list[any], possible_observations: list[any]):
        self.pi = pi
        self.a_ij = a_ij
        self.b = b
        self.states = states
        self.possible_observations = possible_observations

        # TODO: add size checks, dimensions match, etc.

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

    def forward_algorithm(self, observations: list[any]) -> float:
        # $\alpha_t(j) = p(o_1, o_2, ..., o_t, q_t = j | \lambda)$
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
        # TODO: modify using numpy.linalg.multi_dot
        for t in range(1, len(observations)):
            for j in range(len(self.states)):
                # print(t, j, [np.round((alpha[t-1, i], self.a_ij[j, i], self.b[j, observation_indices[t]]), 5) for i in range(len(self.states))])
                alpha[t, j] = sum([(alpha[t-1, i] * self.a_ij[j, i] * self.b[j, observation_indices[t]]) for i in range(len(self.states))])

        # print(alpha)

        # store in alpha for later use
        self.alpha = alpha

        # use np.prod and np.sum across axes
        return np.sum(alpha[-1, :])

    def backward_algorithm(self, observations: list[any]) -> float:
        """
        compute $\beta_t (i) = p(o_{t+1}, o_{t+2}, ..., o_T | q_t = i)$ using reverse of the forward method
        """

        # beta is indexed as t, state, so # observations x # states
        # proabilities start as 1 for state T, so just initializing that here
        beta = np.ones((len(observations), len(self.states)))

        # find indices of the observations in the possible_observations table
        observation_indices = [self.possible_observations.index(o) for o in observations]

        # then, for each step, add a new observation to each path
        
        # $$\beta_t(i) = \sum_{j=1}^n a_{ij} b_j(o_{t+1})\beta_{t+1}(j)$$

        # $$\beta_{t+1} (i)$$ is stored in beta[t+1,i]

        # bad non-numpy method, but it works
        # TODO: modify using numpy.linalg.multi_dot
        for t in range(len(observations)-2, -1, -1): # go through t backwards since b_t depends on b_{t+1}, i.e. T-1, T-2, ..., 0
            for i in range(len(self.states)):
                beta[t, i] = sum([(self.a_ij[j, i] * self.b[j, observation_indices[t+1]] * beta[t+1,j]) for j in range(len(self.states))])

        # store in beta for later use
        self.beta = beta

        # return $$p(O | \lambda) = \sum_{j=1}^n \pi_j b_j(o_1)\beta_1(j)$$ but this is 1-indexed and python is 0-indexed

        return sum([(self.pi[j] * self.b[j, observation_indices[0]] * beta[0,j]) for j in range(len(self.states))])

    def likelihood(self, observations: list[any]) -> float:
        """
        Compute the likelihood of a particular sequence of observations O:  $$\alpha_t(j) = p(o_1, o_2, ..., o_t, q_t = j | \lambda)$$

        There are two ways with N states and a sequence of length T: 
        - the naive method which is $$O(N^T)$$ in naive_likelihood
        - the forward algorithm which is $$O(N^2 T)$$ in forward_algorithm

        This calls the fast forward algorithm.

        Parameters:
        observations: a list of observations, likely strings, numbers, etc. converted to list of indices by the self.possible_observations object

        Returns:
        float of the likelihood, must be between 0 and 1. if you call the method for all possible observation sequences, the probability should sum to 1 (or near it cuz of rounding issues)
        """
        return self.forward_algorithm(observations)

    def decode(self, observations: list[any]) -> tuple[list[int], list[any]]:
            """
            Compute the most probable sequence of states $q_1, ..., q_T$ given series of observations $o_1, ..., o_T$
    
            Uses Viterbi algorithm
    
            This is a similar algorithm to likelihood, except you take the max probability at each step, and track the backsteps
            """
    
            # alpha is indexed as t, state, so # observations x # states
            v_t = np.zeros((len(observations), len(self.states))) # 
            backprop = [0] * len(observations)
            # print(alpha)
    
            # find indices of the observations in the possible_observations table
            observation_indices = [self.possible_observations.index(o) for o in observations]
            # print(observations, observation_indices)
    
            # for each state, compute initial v_t for first step
            initial_v_t = [0.0] * len(self.states)
            for j in range(len(self.states)):
                # get P(state | start) * P(first observation | state)
                v_t[0, j] = self.pi[j] * self.b[j, observation_indices[0]]
                initial_v_t[j] = v_t[0,j]
    
            print(initial_v_t)
            backprop[0] = initial_v_t.index(max(initial_v_t))
    
            # then, for each step, add a new observation to each path
    
            # $$v_t(j) = \max_{i=1}^n v_{t-1}(i) a_{ij} b_j(o_t)$$
    
            # $$v_{t-1} (i)$$ is stored in v_t[t-1,i]
    
            # bad non-numpy method, but it works
            # TODO: modify using numpy.linalg.multi_dot
            for t in range(1, len(observations)):
                max_v_t = 0.0
                max_v_index = -1
                for j in range(len(self.states)):
                    v_t[t, j] = max([(v_t[t-1, i] * self.a_ij[j, i] * self.b[j, observation_indices[t]]) for i in range(len(self.states))])
                    if v_t[t,j] > max_v_t:
                        max_v_t = v_t[t,j]
                        max_v_index = j
                backprop[t] = max_v_index
    
            return backprop, [self.states[state] for state in backprop]

    def visualize_graph(self):
        graph = graphviz.Digraph('hmm', comment='A hidden Markov model')
        graph.attr(rankdir="LR")
        
        # add the state nodes and transition probabilities
        for i, state in enumerate(self.states):
            graph.node(state, f'<{state}<sub>{i}</sub>>')

        # add the edges
        for i, row in enumerate(self.a_ij):
            for j, value in enumerate(row):
                print(self.states[i], self.states[j], value)
                graph.edge(self.states[i], self.states[j], label = str(value))

        # create pi subgraph using HTML table (ChatGPT assistance for this one)
        pi = graphviz.Digraph('hmm', comment='pi probabilities')

        # creates port for edges to be able to be established
        # can access particular cell using "pi:p0:n" for north side, "pi:p0:s" for south side, etc.
        cells = "".join(
            f'<TD PORT="p{i}" CELLPADDING="2">{round(p, 2)}</TD>'
            for i, p in enumerate(self.pi)
        )

        pi.node(
            "pi",
            f'''<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="1">
                <TR>
                    <TD COLSPAN="{len(self.pi)}"><B>&pi;</B></TD>
                </TR>
                <TR>
                    {cells}
                </TR>
            </TABLE>
            >''',
            shape="plain"
        )

        # create the b matrix, also written by ChatGPT
        b = graphviz.Digraph('B', comment='pi probabilities')
        rows = []

        # ports are B:b_0_0 or graph.edge('B', node, tailport="b_0_0:s")
        for i, row in enumerate(self.b):
            cells = "".join(
                f'<TD PORT="b_{i}_{j}" CELLPADDING="4">{value:.2f}</TD>'
                for j, value in enumerate(row)
            )

            rows.append(f"""
                <TR>
                    <TD><B>{self.states[i]}</B></TD>
                    {cells}
                </TR>
            """)

        b.node(
            "B",
            f'''<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                <TR>
                    <TD COLSPAN="{self.b.shape[1] + 1}">
                        <B>B</B>
                    </TD>
                </TR>
                <TR>
                    <TD></TD>
                    {"".join(
                        f"<TD><B>{ob}</B></TD>"
                        for ob in self.possible_observations
                    )}
                </TR>
                {"".join(rows)}
            </TABLE>
            >''',
            shape="plain"
        )

        graph.subgraph(pi)
        graph.subgraph(b)
        graph.render(directory='figure')

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

    hmm.visualize_graph()

    p_o = hmm.naive_likelihood(observations = [3, 1, 3])
    print('naive likelihood', round(p_o, 5))

    # # testing that all possible observations add to 1
    # pos_obs = [(i, j, k) for i in hmm.possible_observations for j in hmm.possible_observations for k in hmm.possible_observations]
    # print("Should sum to 1:", sum([hmm.naive_likelihood(o) for o in pos_obs]))

    # agrees with naive method, nice!
    fast_likelihood = hmm.likelihood([3, 1, 3])
    print('forwards', round(fast_likelihood, 5), 'should be same as backwards', round(hmm.backward_algorithm(observations = [3, 1, 3]), 5))

    dec = hmm.decode(observations = [1,1,3])
    print(dec)

if __name__ == "__main__":
    main()
