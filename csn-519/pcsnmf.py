import numpy as np
import networkx as nx
import random

class PCSNMF:
    # graph
    graph = None

    # Number of communitites
    k = None

    # Adjacency Matrix
    X = None

    # must-link pairwisely constrainted symmetric matrix
    M = None

    # cannot-link pairwisely constrainted symmetric matrix
    C = None

    # Diagonal Zero Matrix
    B = None

    # nodes to sample
    f = 6

    # Number of nodes
    n = None

    alpha = 0.0005

    def __init__(self, graph, k) -> None:
        self.graph = graph
        self.k = k
        self.n = len(self.graph.nodes())
        self._create_base_matrix()
        self._random_node_sampling()


    def _random_node_sampling(self):
        nodes = random.sample(self.graph.nodes(), self.f)

        self.M = np.zeros((self.n, self.n))
        self.C = np.zeros((self.n, self.n))
        self.B = np.ones((self.k, self.k))

        for i in range(self.k):
            self.B[i][i] = 0

        for i in nodes:
            for j in nodes:
                if i == j:
                    continue
                label1 = self.graph.nodes()[i]['club']
                label2 = self.graph.nodes()[j]['club']
                if label1 == label2:
                    self.M[i][j] = 1
                else:
                    self.C[i][j] = 1

    def _create_base_matrix(self):
        self.X = nx.to_numpy_array(self.graph, weight = None)
        for i in range(self.n):
            self.X[i][i] = 1

    def _update_matrix_variable(self, S):
        Xt = np.transpose(self.X)
        St = np.transpose(S)

        Xt_S = np.dot(Xt,S)
        S_St_S = np.dot(np.dot(S, St), S)
        M_S_B = np.dot(np.dot(self.M, S), self.B)
        C_S = np.dot(self.C, S)
        M_S_B_C_S = M_S_B + C_S

        for i in range(self.n):
            for c in range(self.k):
                fac = (2*Xt_S[i][c]) / (2*S_St_S[i][c] + self.alpha * M_S_B_C_S[i][c])
                if(fac == np.nan):
                    fac = 0.0
                S[i][c] *= fac

    def detect(self):
        S = np.random.rand(self.n, self.k)

        for iteration in range(200):
            self._update_matrix_variable(S)
        return S

    def get_communities(self):
        S = self.detect()
        communities = S.argmax(axis=1)
        return communities


graph = nx.karate_club_graph()
model = PCSNMF(graph, 2)
arr = [-1] * 34
for node in graph.nodes():
    txt = graph.nodes()[node]["club"]
    if (txt == "Mr. Hi"):
        arr[node] = 0
    else:
        arr[node] = 1

print(model.get_communities(), "Detected")
print(np.array(arr), "Actual")
