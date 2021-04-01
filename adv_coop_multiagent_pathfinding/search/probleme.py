# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:32:05 2016

@author: nicolas
"""

import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod
import functools
import time
from search.grid3D import ProblemeGrid3D
import itertools


def distManhattan(p1, p2):
    """ calcule la distance de Manhattan entre le tuple
        p1 et le tuple p2
        """
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(x1-x2)+abs(y1-y2)


###############################################################################

class Probleme(object):
    """ On definit un probleme comme étant:
        - un état initial
        - un état but
        - une heuristique
        """

    def __init__(self, init, but, heuristique):
        self.init = init
        self.but = but
        self.heuristique = heuristique

    @abstractmethod
    def estBut(self, e):
        """ retourne vrai si l'état e est un état but
            """
        pass

    @abstractmethod
    def cost(self, e1, e2):
        """ donne le cout d'une action entre e1 et e2,
            """
        pass

    @abstractmethod
    def successeurs(self, etat):
        """ retourne une liste avec les successeurs possibles
            """
        pass

    @abstractmethod
    def immatriculation(self, etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        pass


###############################################################################

@functools.total_ordering  # to provide comparison of nodes
class Noeud:
    def __init__(self, etat, g, pere=None):
        self.etat = etat
        self.g = g
        self.pere = pere

    def __str__(self):
        # return np.array_str(self.etat) + "valeur=" + str(self.g)
        return str(self.etat) + " valeur=" + str(self.g)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def expand(self, p):
        """ étend un noeud avec ces fils
            pour un probleme de taquin p donné
            """
        nouveaux_fils = [Noeud(s, self.g+p.cost(self.etat, s), self)
                         for s in p.successeurs(self.etat)]
        return nouveaux_fils

    def expandNext(self, p, k):
        """ étend un noeud unique, le k-ième fils du noeud n
            ou liste vide si plus de noeud à étendre
            """
        nouveaux_fils = self.expand(p)
        if len(nouveaux_fils) < k:
            return []
        else:
            return self.expand(p)[k-1]

    def trace(self, p):
        """ affiche tous les ancetres du noeud
            """
        n = self
        c = 0
        while n != None:
            print(n)
            n = n.pere
            c += 1
        print("Nombre d'étapes de la solution:", c-1)
        return


###############################################################################
# A*
###############################################################################

def astar(p, verbose=False, stepwise=False):
    """
    application de l'algorithme a-star
    sur un probleme donné
        """

    startTime = time.time()

    nodeInit = Noeud(p.init, 0, None)
    frontiere = [(nodeInit.g+p.h_value(nodeInit.etat, p.but), nodeInit)]

    reserve = {}
    bestNoeud = nodeInit

    while frontiere != [] and not p.estBut(bestNoeud.etat):
        (min_f, bestNoeud) = heapq.heappop(frontiere)

    # VERSION 1 --- On suppose qu'un noeud en réserve n'est jamais ré-étendu
    # Hypothèse de consistence de l'heuristique
        if p.immatriculation(bestNoeud.etat) not in reserve:
            reserve[p.immatriculation(bestNoeud.etat)
                    ] = bestNoeud.g  # maj de reserve
            nouveauxNoeuds = bestNoeud.expand(p)
            for n in nouveauxNoeuds:
                f = n.g+p.h_value(n.etat, p.but)
                heapq.heappush(frontiere, (f, n))

    # TODO: VERSION 2 --- Un noeud en réserve peut revenir dans la frontière

        stop_stepwise = ""
        if stepwise == True:
            stop_stepwise = input("Press Enter to continue (s to stop)...")
            print("best", min_f, "\n", bestNoeud)
            print("Frontière: \n", frontiere)
            print("Réserve:", reserve)
            if stop_stepwise == "s":
                stepwise = False

    # Mode verbose
    # Affichage des statistiques (approximatives) de recherche
    # et les differents etats jusqu'au but
    if verbose:
        bestNoeud.trace(p)
        print("=------------------------------=")
        print("Nombre de noeuds explorés", len(reserve))
        c = 0
        for (f, n) in frontiere:
            if p.immatriculation(n.etat) not in reserve:
                c += 1
        print("Nombre de noeuds de la frontière", c)
        print("Nombre de noeuds en mémoire:", c + len(reserve))
        print("temps de calcul:", time.time() - startTime)
        print("=------------------------------=")

    n = bestNoeud
    path = []
    while n != None:
        path.append(n.etat)
        n = n.pere
    return path[::-1]  # extended slice notation to reverse list


###############################################################################
# AUTRES ALGOS DE RESOLUTIONS...
###############################################################################

def coop_astar(inits, buts, grid, time_limit, verbose=False, stepwise=False):
    """
    application de l'algorithme a-star
    sur un probleme donné
        """
    reserved = []
    paths = []
    for init, but in zip(inits, buts):
        new_problem = ProblemeGrid3D(
            init, but, grid, "manhattan", reserved, time_limit)
        path = astar(new_problem, True)
        paths.append(path)
        for (x, y, t) in path:
            reserved.append((x, y, t))
            reserved.append((x, y, t + 1))
        for delta_t in range(time_limit-path[-1][2]):
            reserved.append((path[-1][0], path[-1][1], t+delta_t))
    return paths


#############################################
# Alpha Beta Pruning
#############################################

class GameNode:
    def __init__(self, team_states, depth, value=0, parent=None):
        # a numpy array False for walls True for empty cell, 'xij' for player j of team i, 'yij' for goal j of team i
        self.team_states = team_states  # dictionary for team 0 and 1 agents states
        self.depth = depth
        self.value = value    # an int
        self.parent = parent  # a node reference
        self.children = []    # a list of nodes

    def addChild(self, childNode):
        self.children.append(childNode)


class GameTree:
    def __init__(self):
        self.root = None

    def build_tree(self, map, team_states, team_goal_states, depth_limit):
        """
        :param data_list: Take data in list format
        :return: Parse a tree from it
        """
        self.map = map
        self.team_states = team_states
        self.team_goal_states = team_goal_states
        self.depth_limit = depth_limit
        self.root = GameNode(team_states, 0)
        self.parse_subtree(team_states, self.root)

    def legal_position(self, rowcol, team_states):
        if(rowcol[0] >= 0 and rowcol[0] < self.map.shape[0] and rowcol[1] >= 0 and rowcol[1] < self.map.shape[1]):
            if self.map[rowcol] == True:
                if not(rowcol in team_states['0']) and not(rowcol in team_states['1']):
                    return True
        return False

    def possible_positions_from_a_state(self, rowcol, team_states):
        possible_states = []
        for dir in [(1, 0), (0, -1), (-1, 0), (0, 1), (0, 0)]:
            next_state = tuple(np.add(rowcol, dir))
            if self.legal_position(next_state, team_states) or next_state == rowcol:
                possible_states.append(next_state)
        return possible_states

    def all_possible_position_combinations(self, team_states, team):
        possible_states_array = []
        for agent_state in team_states[team]:
            possible_states_array.append(
                self.possible_positions_from_a_state(agent_state, team_states))
        combinations = list(itertools.product(*possible_states_array))
        for elem in combinations:
            if len(set(elem)) != len(elem):
                combinations.remove(elem)
        return combinations

    def new_team_states(self, team_states, team):
        team_states_list = []
        temp_dict = team_states.copy()
        combinations = self.all_possible_position_combinations(
            team_states, team)
        for combination in combinations:
            temp_dict[team] = combination
            team_states_list.append(temp_dict.copy())
        return team_states_list

    def parse_subtree(self, team_states, parent):
        # base case
        if parent.depth == self.depth_limit-1:
            # if we're at a leaf, set the value
            team = '1' if parent.depth % 2 else '0'
            for new_team_states in self.new_team_states(team_states, team):
                leaf_node = GameNode(new_team_states, parent.depth+1)
                # make connections
                leaf_node.parent = parent
                parent.addChild(leaf_node)
                score = 0
                for i in range(len(leaf_node.team_states['0'])):
                    if leaf_node.team_states['0'][i] == self.team_goal_states['0'][i]:
                        score += 1
                for i in range(len(leaf_node.team_states['1'])):
                    if leaf_node.team_states['1'][i] == self.team_goal_states['1'][i]:
                        score -= 1
                leaf_node.value = score
                """if score == 2:
                    my_node = leaf_node
                    print(leaf_node.team_states, score, leaf_node.depth)
                    print(my_node.team_states, my_node.depth)
                    while my_node.parent != self.root:
                        print(my_node.parent.team_states, my_node.parent.depth)
                        my_node = my_node.parent"""
            return
        # recursive case
        team = '1' if parent.depth % 2 else '0'
        for new_team_states in self.new_team_states(team_states, team):
            tree_node = GameNode(new_team_states, parent.depth+1)
            # make connections
            tree_node.parent = parent
            parent.addChild(tree_node)
            self.parse_subtree(new_team_states, tree_node)

        # return from entire method if base case and recursive case both done running
        return


##########################
###### MINI-MAX     ######
##########################

class MiniMax:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree, isMin=False):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.isMin = isMin  # if root node is Minimizing node reverse the values
        self.currentNode = None     # GameNode
        self.successors = []        # List of GameNodes
        return

    def minimax(self, node):
        # first, find the max value
        best_val = self.max_value(node)  # should be root node of tree

        # second, find the node which HAS that max value
        #  –> means we need to propagate the values back up the
        #      tree as part of our minimax algorithm
        successors = self.getSuccessors(node)
        print("MiniMax:  Utility Value of Root Node: = " + str(best_val))
        # find the node with our best move
        best_move = None
        for elem in successors:   # —> Need to propagate values up tree for this to work
            my_value = -elem.value if self.isMin else elem.value
            if elem.value == best_val:
                best_move = elem
                break

        # return that best value that we've found
        return best_move

    def max_value(self, node):
        #print("MiniMax–>MAX: Visited Node :: ", node.team_states, node.value, self.isTerminal(node))
        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        max_value = -infinity

        successors_states = self.getSuccessors(node)
        for state in successors_states:
            max_value = max(max_value, self.min_value(state))
        return max_value

    def min_value(self, node):
        #print("MiniMax–>MIN: Visited Node :: ", node.team_states, node.value, self.isTerminal(node))
        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        min_value = infinity

        successor_states = self.getSuccessors(node)
        for state in successor_states:
            min_value = min(min_value, self.max_value(state))
        return min_value

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes…
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        if self.isMin:
            return -node.value
        else:
            return node.value


##########################
###### MINI-MAX A-B ######
##########################

class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree, isMin=False):
        self.game_tree = game_tree  # GameTree
        self.isMin = isMin  # if root node is Minimizing node reverse the values
        self.root = game_tree.root  # GameNode
        return

    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = - infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
        print("AlphaBeta:  Best State is: ", best_state.team_states)
        return best_state

    def max_value(self, node, alpha, beta):
        #print("AlphaBeta–>MAX: Visited Node :: " , node.team_states)
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        #print("AlphaBeta–>MIN: Visited Node :: ", node.team_states)
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes…
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        if self.isMin:
            return -node.value
        else:
            return node.value
