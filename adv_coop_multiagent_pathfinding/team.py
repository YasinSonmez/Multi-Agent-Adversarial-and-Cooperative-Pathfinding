from search.grid2D import ProblemeGrid2D
from search import probleme
import random
import numpy as np


def legal_position(rowcol, map, team_states):
    # une position legale est dans la carte et pas sur un mur
    if not ((rowcol in team_states['0']) and (rowcol in team_states['1']) and rowcol[0] >= 0 and rowcol[0] < map.shape[0] and rowcol[1] >= 0 and rowcol[1] < map.shape[1]):
        return False
    else:
        return map[rowcol]


class Team():
    """ Team with agents. Holds the agents and organizes their movement within
    the team.
    """

    def __init__(self, strategy, agents, iterations=10, id='0'):
        self.strategy = strategy
        self.agents = agents
        self.id = id
        for agent in self.agents:
            agent.update_strategy(self.strategy)
        self.initial_states = [agent.initial_state for agent in self.agents]
        self.goal_states = [agent.goal_state for agent in self.agents]
        self.team_goal_states = None
        self.current_states = [agent.current_state for agent in self.agents]
        self.iterations = iterations
        self.score = 0

    def update_positions(self, team_states, i, game_node=None):
        self.i = i
        if (i == 0) and self.strategy == 'Cooperative A*':
            self.coop_astar_update_path(self.agents[0].map)
        if self.strategy == 'Alpha-Beta':
            if i == 0 and self.id == '0':
                global my_game
                my_game = probleme.GameTree()
                my_game.build_tree(
                    self.agents[0].map, team_states, self.team_goal_states, 2*self.iterations)
            if game_node is None:
                game_node = my_game.root
            isMin = True if self.id == '1' else False
            new_node = probleme.AlphaBeta(
                my_game, isMin).alpha_beta_search(game_node)
            for agent in self.agents:
                agent.current_state = new_node.team_states[self.id][agent.id]
                agent.i = i
                team_states[self.id][agent.id] = agent.current_state
            return new_node
        for agent in self.agents:
            if not agent.score:  # If not yet reached to goal position update
                agent.update_position(team_states, i)

    def coop_astar_update_path(self, map):
        goal_states = [tuple(list(goal_state)+[0])
                       for goal_state in self.goal_states]
        current_states_temp = [agent.current_state
                               for agent in self.agents]
        current_states = [tuple(list(current_state)+[0])
                          for current_state in current_states_temp]
        self.coop_paths = probleme.coop_astar(current_states,
                                              goal_states, map, self.iterations)
        for agent, coop_path in zip(self.agents, self.coop_paths):
            # agent.path = coop_path
            agent.path = agent.path[:self.i] + coop_path[1:]
            print(self.i)


class Agent():
    """ Agent with a strategy. Holds the current, initial, goal position and
    path in memory.
    """

    def __init__(self, initial_state, goal_state, map, players_id, agent_id='0', team=None):
        self.initial_state = initial_state
        self.current_state = initial_state
        self.goal_state = goal_state
        self.map = map
        self.players_id = players_id
        self.score = 0
        self.id = agent_id
        self.team = team
        self.path = []
        self.i = 0

    def update_strategy(self, strategy):
        self.strategy = strategy

    def calculate_path(self, map=None):
        if map is None:
            map = self.map
        if (self.strategy == 'A*' or self.strategy == 'A* update every step' or
                self.strategy == 'Local A*'):
            p = ProblemeGrid2D(self.current_state,
                               self.goal_state, map, 'manhattan')
            self.path = self.path[:self.i] + probleme.astar(p)[1:]

        if (self.strategy == 'Cooperative A*'):
            self.team.coop_astar_update_path(map)

    def next_step(self, team_states, i=None):
        # Move to next grid in path or stay put if no path is returned
        if i is None:
            i = self.i
        if (self.current_state[0:2] == self.goal_state[0:2]):
            return self.current_state
        if len(self.path) > i:
            return self.path[i][0:2]
        else:
            for dir in [(1, 0), (0, -1), (-1, 0), (0, 1), (0, 0)]:
                next_state = tuple(
                    np.add(self.current_state[0:2], dir))
                if legal_position(next_state, self.map, team_states):
                    return next_state
        return self.current_state

    def update_position(self, team_states, i):
        """Updates the position of the agent and if the goal is reached
        returns True """
        self.i = i  # change the current step

        # if the goal is reached end the game
        if (self.current_state[0:2] == self.goal_state[0:2]):
            print("un joueur d'equipe " + str(self.team.id) + " with strategy = " +
                  self.strategy + " a atteint son but!")
            self.score += 1
            return

        if (self.strategy == 'A*'):
            if i == 0:
                self.calculate_path(self.map)
            self.current_state = self.path[i]

        if (self.strategy == 'A* update every step'):
            self.calculate_path()
            self.current_state = self.path[i]

        if (self.strategy == 'Local A*'):
            if i == 0:
                self.calculate_path()

            rowcol = self.next_step(team_states)
            dynamic_map = self.map.copy()
            # if there is collision in next step
            while ((rowcol in team_states['0']) or (rowcol in team_states['1'])) and rowcol != self.current_state:
                dynamic_map[rowcol] = False
                self.calculate_path(dynamic_map)
                rowcol = self.next_step(team_states)
            self.current_state = rowcol

        if (self.strategy == 'Cooperative A*'):
            rowcol = self.next_step(team_states)
            # if there is collision in next step recalculate
            # allyStates = [agent.current_state[0:2]
            #              for agent in self.team.agents]
            allyNextStates = [agent.next_step(team_states, self.i)[0:2]
                              for agent in self.team.agents]  # change this
            if rowcol[0:2] in allyNextStates:
                allyNextStates.remove(rowcol[0:2])

            # using xor to change 1 to 0 and vice versa
            opponent_team_id = str(int(self.team.id) ^ 1)
            opponentStates = team_states[opponent_team_id]
            dynamic_map = self.map.copy()
            while (rowcol in opponentStates) or (rowcol in allyNextStates) and rowcol != self.current_state:
                dynamic_map[rowcol] = False
                self.calculate_path(dynamic_map)
                rowcol = self.next_step(team_states)
            self.current_state = rowcol

        team_states[self.team.id][self.id] = self.current_state
