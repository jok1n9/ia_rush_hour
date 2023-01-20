
# Module: tree_search
#
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
import asyncio
# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc


class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial):
        self.domain = domain
        self.initial = initial

    def goal_test(self, state):
        return self.domain.satisfies(state)

# Nos de uma arvore de pesquisa


class SearchNode:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.cost = 0
        self.heuristic = 0
        self.actions = []
        self.highest_cost_nodes = []
        self.depth = 0

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"

    def __repr__(self):
        return str(self)

# Arvores de pesquisa


class SearchTree:

    # construtor
    def __init__(self, problem, strategy='breadth'):
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.known = set()

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self, node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return (path)

    def get_path_nodes(self, node):
        if node.parent == None:
            return [node]
        nodes = self.get_path_nodes(node.parent)
        nodes += [node]
        return (nodes)

    @property
    def length(self):
        return self.solution.depth

    @property
    def avg_branching(self):
        return (self.terminals+self.non_terminals-1)/self.non_terminals

    @property
    def cost(self):
        return self.solution.cost

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:

            node = self.open_nodes.pop(0)
            if node.parent != None:
                self.known.add(str(node.state))
            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path_nodes(node)
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                if str(newstate) not in self.known:
                    newnode = SearchNode(newstate, node)
                    newnode.depth += node.depth+1
                    newnode.actions = node.actions + [a]
                    newnode.heuristic = self.problem.domain.heuristic(newstate)
                    self.known.add(str(newstate))
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self, lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(
                self.open_nodes + lnewnodes, key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes = sorted(
                self.open_nodes + lnewnodes, key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes = sorted(
                self.open_nodes + lnewnodes, key=lambda node: node.cost + node.heuristic)
