# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain

import time
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
import matplotlib.pyplot as plt

game = Game()


def init(_boardname=None):
    global player, game
    name = _boardname if _boardname is not None else 'demoMap'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 50  # frames per second
    game.mainiteration()
    player = game.player


def play_a_game():
    # for arg in sys.argv:
    iterations = 30  # default
    if len(sys.argv) == 4:
        iterations = int(sys.argv[1])
    print("Iterations: ", iterations)

    init('exAdvCoopMap')

    # -------------------------------
    # Initialisation
    # -------------------------------

    nbLignes = game.spriteBuilder.colsize
    nbCols = game.spriteBuilder.rowsize

    print("lignes", nbLignes)
    print("colonnes", nbCols)

    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)

    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print("Init states:", initStates)

    # on localise tous les objets ramassables
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    # goalStates = goalStates[::-1]
    random.shuffle(goalStates)
    print("Goal states:", goalStates)

    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print("Wall states:", wallStates)

    # par defaut la matrice comprend des True
    map = np.ones((nbLignes, nbCols), dtype=bool)
    for w in wallStates:            # putting False for walls
        map[w] = False

    # define team strategies
    # strategies = ['Local A*', 'Local A*']
    strategies = ['Local A*', 'Cooperative A*']
    # strategies = ['Alpha-Beta', 'Alpha-Beta']

    agents = []
    for i in range(nbPlayers):
        agents.append(Agent(initStates[i], goalStates[i], map, players_id=i))

    teams = []

    # Determine teams of the agents automatically
    random.shuffle(agents)
    teams.append(
        Team(strategies[0], agents[:int(nbPlayers/2)], iterations, '0'))
    teams.append(
        Team(strategies[1], agents[int(nbPlayers/2):], iterations, '1'))

    # Determine teams of the agents by hand
    # if allies
    # teams.append(Team(strategies[0], [agents[0], agents[1]], iterations, '0'))
    # teams.append(Team(strategies[0], [], iterations, '1'))

    # if enemies
    # teams.append(Team(strategies[0], [agents[1]], iterations, '0'))  # Team 0
    # teams.append(Team(strategies[0], [agents[0]], iterations, '1'))  # Team 1

    # give every agent it's team and create team_states dictionary
    global team_states, team_goal_states
    team_states = {'0': [], '1': []}
    team_goal_states = {'0': [], '1': []}
    for team in teams:
        for i, agent in enumerate(team.agents):
            team_states[team.id].append(agent.initial_state)
            team_goal_states[team.id].append(agent.goal_state)
            agent.team = team
            agent.id = i
    teams[0].team_goal_states = team_goal_states
    teams[1].team_goal_states = team_goal_states

    # -------------------------------
    # Boucle principale de déplacements
    # -------------------------------
    new_game_node = None
    for i in range(iterations):
        for team in teams:
            new_game_node = team.update_positions(
                team_states, i, new_game_node)
            for agent in team.agents:
                row, col = agent.current_state[0:2]
                players[agent.players_id].set_rowcol(row, col)
            print(team_states, i)
            game.mainiteration()  # on passe a l'iteration suivante du jeu
    for team in teams:
        for agent in team.agents:
            team.score += agent.score
        print('Equipe '+str(team.id) + ' avec strategie ' +
              str(team.strategy)+' a gagne ' + str(team.score) + ' points.')
    pygame.quit()

    return [teams[0].score, teams[1].score]
    # -------------------------------


def main():
    team0_scores = []
    team1_scores = []
    for _ in range(1):
        score0, score1 = play_a_game()
        team0_scores.append(score0)
        team1_scores.append(score1)

    """t = range(len(team0_scores))
    print(t, np.cumsum(team0_scores), np.cumsum(team1_scores))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(t, np.cumsum(team0_scores), label='Local A*')
    ax.plot(t, np.cumsum(team1_scores), label='Cooperative A*')
    ax.legend()
    plt.show()"""
    return


if __name__ == '__main__':
    main()
