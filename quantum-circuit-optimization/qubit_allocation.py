import random

class Allocation:

    def __init__(self):
        # linear topology i.e. [0,1,2,3]
        # connectivity would be (0,1) (1,0) (1,2) (2,1) (2,3) (3,2)
        self.topology = []
        self.qubits = 4

    @property
    def qubit_allocation(self):
        # allocation random assigned
        # self.topology = (random.sample(range(self.qubits), 4))
        # print(self.topology)

        # self-assigned qubit allocation for testing
        for i in range(self.qubits):
            self.topology.append(i)

        return self.topology

    def connectivity(self):

        topology = self.topology
        connectivity_set = []

        for i, obj in enumerate(topology):

            if i == 0:
                connectivity_set.append([obj, topology[i + 1]])
            elif i == (len(topology)-1):
                connectivity_set.append([obj, topology[i - 1]])
            else:
                connectivity_set.append([obj, topology[i - 1]])
                connectivity_set.append([obj, topology[i + 1]])

        return connectivity_set

# a = Allocation()
# a.qubit_allocation
# a.connectivity()


