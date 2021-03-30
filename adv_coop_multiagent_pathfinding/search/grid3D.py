import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod


def distManhattan(p1, p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(x1-x2)+abs(y1-y2)


###############################################################################

class ProblemeGrid3D():
    """ On definit un probleme de labyrithe comme étant: 
        - n états initials
        - n états buts
        - une grid, donné comme un array booléen (False: obstacle)
        - une heuristique (supporte Manhattan, euclidienne)
        """

    def __init__(self, init, but, grid, heuristique, reserved=None):
        self.init = init
        self.but = but
        self.grid = grid
        self.heuristique = heuristique
        self.reserved = reserved

    def cost(self, e1, e2):
        """ donne le cout d'une action entre e1 et e2, 
            toujours 1 pour le taquin
            """
        return 1

    def estBut(self, e):
        """ retourne vrai si l'état e est un état but
            """
        return (self.but[0:2] == e[0:2])

    def estObstacle(self, e):
        """ retorune vrai si l'état est un obsacle
            """
        return (self.grid[e[0:2]] == False)

    def estDehors(self, etat):
        """retourne vrai si en dehors de la grille
            """
        (s, t) = self.grid.shape
        (x, y) = etat[0:2]
        return ((x >= s) or (y >= t) or (x < 0) or (y < 0))

    def estReserved(self, etat):
        """retourne vrai si en dehors de la grille
            """
        if self.reserved is None:
            return False
        else:
            return (etat in self.reserved)

    def successeurs(self, etat):
        """ retourne des positions successeurs possibles
            """
        current_x, current_y, current_t = etat
        d = [(0, 1, 1), (1, 0, 1), (0, -1, 1), (-1, 0, 1), (0, 0, 1)]
        etatsApresMove = [(current_x+inc_x, current_y+inc_y, current_t+inc_t)
                          for (inc_x, inc_y, inc_t) in d]
        return [e for e in etatsApresMove if not(self.estDehors(e)) and not(self.estObstacle(e)) and not(self.estReserved(e))]

    def immatriculation(self, etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        s = ""
        (x, y, t) = etat
        s += str(x)+str(y)+str(t)
        return s

    def h_value(self, e1, e2):
        """ applique l'heuristique pour le calcul 
            """
        if self.heuristique == 'manhattan':
            h = distManhattan(e1[0:2], e2[0:2])
        elif self.heuristique == 'uniform':
            h = 1
        return h
