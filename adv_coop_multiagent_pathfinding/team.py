from search.grid2D import ProblemeGrid2D
from search import probleme
import random
import numpy as np


def legal_position(rowcol, map):
    # une position legale est dans la carte et pas sur un mur
    if not (rowcol[0] >= 0 and rowcol[0] < map.shape[0] and rowcol[1] >= 0 and rowcol[1] < map.shape[1]):
        return False
    else:
        return map[rowcol]


class Team():
    """ Team with agents. Holds the agents and organizes their movement within
    the team.
    """

    def __init__(self, strategy, agents, iterations=10):
        self.strategy = strategy
        self.agents = agents
        for agent in self.agents:
            agent.update_strategy(self.strategy)
        self.initial_states = [agent.initial_state for agent in self.agents]
        self.goal_states = [agent.goal_state for agent in self.agents]
        self.map = agents[0].map

    def update_positions(self, playerStates, i):
        if self.strategy == 'Cooperative A*' and i == 0:
            self.coop_astar_update_path()

        for agent in self.agents:
            if not agent.score:  # If not yet reached to goal position update
                agent.update_position(playerStates, i)

    def coop_astar_update_path(self):
        initial_states = [tuple(list(initial_state)+[0])
                          for initial_state in self.initial_states]
        goal_states = [tuple(list(goal_state)+[0])
                       for goal_state in self.goal_states]
        self.coop_paths = probleme.coop_astar(initial_states,
                                              goal_states, self.map, 100)
        for agent, coop_path in zip(self.agents, self.coop_paths):
            agent.path = coop_path


class Agent():
    """ Agent with a strategy. Holds the current, initial, goal position and
    path in memory.
    """

    def __init__(self, initial_state, goal_state, map, agent_id, team=None):
        self.initial_state = initial_state
        self.current_state = initial_state
        self.goal_state = goal_state
        self.map = map
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

    def next_step(self):
        # Move to next grid in path or stay put if no path is returned
        if len(self.path) > self.i:
            return self.path[self.i]
        else:
            while True:
                random_dir = random.choice(
                    [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)])
                next_state = tuple(np.add(self.current_state[0:2], random_dir))
                if legal_position(next_state, self.map):
                    return next_state

    def update_position(self, playerStates, i):
        """Updates the position of the agent and if the goal is reached
        returns True """
        self.i = i  # change the current step

        # if the goal is reached end the game
        if (self.current_state[0:2] == self.goal_state[0:2]):
            print("le joueur " + str(self.id) + " with strategy = " +
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

            rowcol = self.next_step()
            dynamic_map = self.map.copy()
            # if there is collision in next step
            while (rowcol in playerStates.values()) and rowcol != self.current_state:
                dynamic_map[rowcol] = False
                self.calculate_path(dynamic_map)
                rowcol = self.next_step()
            self.current_state = rowcol

        if (self.strategy == 'Cooperative A*'):
            self.current_state = self.next_step()

        playerStates[str(self.id)] = self.current_state
