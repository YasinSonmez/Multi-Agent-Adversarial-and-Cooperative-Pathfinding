# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain

import pygame

from pySpriteWorld.gameclass import Game, check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme
from team import Agent, Team


# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----


# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()


def init(_boardname=None):
    global player, game
    name = _boardname if _boardname is not None else 'demoMap'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 2  # frames per second
    game.mainiteration()
    player = game.player


def main():
    # for arg in sys.argv:
    iterations = 10  # default
    if len(sys.argv) == 4:
        iterations = int(sys.argv[1])
    print("Iterations: ")
    print(iterations)

    init('map1')

    # -------------------------------
    # Initialisation
    # -------------------------------

    nbLignes = game.spriteBuilder.colsize
    nbCols = game.spriteBuilder.rowsize

    print("lignes", nbLignes)
    print("colonnes", nbCols)

    nbTeams = 2
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers

    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print("Init states:", initStates)

    # on localise tous les objets ramassables
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print("Goal states:", goalStates)

    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print("Wall states:", wallStates)

    global playerStates
    playerStates = {}

    # par defaut la matrice comprend des True
    map = np.ones((nbLignes, nbCols), dtype=bool)
    for w in wallStates:            # putting False for walls
        map[w] = False

    # define team strategies
    strategies = ['A* update if collision in next step',
                  'A* update if collision in next step']
    # strategies = ['A* update every step', 'A* update every step']
    # strategies = ['A*', 'A*']
    goalStates = goalStates[:: -1]
    agents = []
    for i in range(nbPlayers):
        agents.append(Agent(initStates[i], goalStates[i], i))
        playerStates[str(i)] = initStates[i]

    teams = []
    # for i in range(nbTeams):
    #    teams.append(Team(strategies[i], [agents[i]]))
    teams.append(Team(strategies[0], [agents[0], agents[1]]))
    # -------------------------------
    # Boucle principale de déplacements
    # -------------------------------
    game_ended = False
    for i in range(iterations):
        if game_ended:
            break
        for team in teams:
            if team.update_positions(map, playerStates, i):
                game_ended = True
                break
            for agent in team.agents:
                row, col = agent.current_state
                players[agent.id].set_rowcol(row, col)
            # on passe a l'iteration suivante du jeu
            game.mainiteration()

    # print("scores:", score)
    pygame.quit()

    # -------------------------------


if __name__ == '__main__':
    main()
