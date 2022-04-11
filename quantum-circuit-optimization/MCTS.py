import itertools
from math import log, sqrt, e, inf

# TODO: FIND SHORTEST PATH TO LEAF NODE
from agent import Agent
from circuit import Circuit
from qubit_allocation import Allocation
from types import SimpleNamespace

import random


class Node:
    def __init__(self, parent=None):
        self.reward = 1
        self.N = 1
        self.n = 0
        self.children: list[Node] = []
        self.parent = parent
        #self.action = action


class MCTS:

    def __init__(self, agent, circuit):
        self.state = agent.scheduled_gates
        # print(f'the state is {self.state}')# a circuit [[0,1,0],[1,0,0]] from first action
        # self.constraints = allocation_class.connectivity()
        self.reward = 0
        # self.action = 0  #
        self.parent = 0
        self.N = 0
        self.n = 0
        self.n_qubits = circuit.n_qubits
        self.root = Node()

    # Node is a circuit with gates, parent node should change for every action, child node is the possible action
    # coming from parent node
    @property
    def action(self):
        possible_action = []
        for i, j in pairwise(list(range(self.n_qubits))):
            swap_gate = [i, j, 1]
            possible_action.append(swap_gate)

        # print(possible_action)
        return possible_action

    def ucb(self, node_i):
        """
        Upper Confidence Bound for selecting the best child node
        """
        # node_i = SimpleNamespace(**node_i)
        #
        # mean_reward = node_i.reward
        # num_parent_visits = node_i.N
        # num_child_visits = node_i.n
        #wortel 2
        ucb = node_i.reward + 2 * (sqrt(log(node_i.N + e + (10 ** (-6))) / (node_i.n + 10 ** (-1))))
        return ucb

    def swap_schedule(self, i, end_state, gate):

        #(ADD: constraint not two swaps next to each other)

        a, b, _ = i

        if gate[0] > gate[1]:
            distance = gate[0] - gate[1]
        else:
            distance = gate[1] - gate[0]

        new_gate = [gate[0], gate[1]]

        for x in range(len(new_gate)):
            if new_gate[x] == a:
                new_gate[x] = b
            elif new_gate[x] == b:
                new_gate[x] = a

        if new_gate[0] > new_gate[1]:
            new_distance = new_gate[0] - new_gate[1]
        else:
            new_distance = new_gate[1] - new_gate[0]

        print(f'distance is {new_distance}')
        # Reward for improving the CNOT
        if new_distance < distance:
            reward = 5
        elif new_distance == 1:
            reward = 100
            end_state = True
        else:
            reward = -1

        print(f'reward is {reward}')

        return end_state, reward, new_gate

    def selection(self, gate):
        # receives iteration
        # choosing child node based on Upper Confidence Bound
        """
        Iterate through all the child of the given state and select the one with highest UCB value
        """

        # get parent node and child_nodes is the one with all the calculated actions
        action = self.action

        end_state = False
        for i in action:
            self.root.children.append(i)

        circuit = []
        while not end_state:
            best_action = self.select_leaf(self.root)

            end_state, reward, new_gate = self.swap_schedule(best_action, end_state, gate)

            circuit.append(new_gate)

        print(circuit)
        return end_state

    # function for the result of the simulation
    def rollout(self, node):
        # while non_terminal(node):
        #     node = rollout_policy(node)
        # return result(node)
        return

    # function for randomly selecting a child node
    def rollout_policy(self, node):
        # return pick_random(node.children)
        return

    # function for backpropagation
    def backpropagation(self, node, result):
        # if is_root(node) return
        # node.stats = update_stats(node, result)
        # backpropagation(node.parent)
        return

    # function for selecting the best child
    # node with the highest number of visits
    def best_child(self, node):
        # pick
        # child
        # with the highest number of visits
        return


    def select_leaf(self, root):

        while bool(root.children):
            children = root.children
            print(children)
            best = None
            best_ucb = inf
            for child in children:
                print(child)
                ucb = self.ucb(child)

                if ucb < best_ucb:
                    best_ucb = ucb
                    best = child
            root = best
        return root


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


c = Circuit(4)
all = Allocation()
con = all.connectivity()
circ = c.get_circuit()

a = Agent()
for i in circ:
    if not a.schedule_gate(con, i):
        break

m = MCTS(a, c)
t = [3, 0, 0]
m.selection(t)
