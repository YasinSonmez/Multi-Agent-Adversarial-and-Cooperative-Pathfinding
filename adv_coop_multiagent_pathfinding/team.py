from search.grid2D import ProblemeGrid2D
from search import probleme


class Team():
    """ Team with agents. Holds the agents and organizes their movement within 
    the team.
    """

    def __init__(self, strategy, agents):
        self.strategy = strategy
        self.agents = agents
        for agent in self.agents:
            agent.update_strategy(self.strategy)

    def update_positions(self, map, playerStates, i):
        for agent in self.agents:
            if not agent.score:  # If not yet reached to goal position update
                agent.update_position(map, playerStates, i)
        return False


class Agent():
    """ Agent with a strategy. Holds the current, initial, goal position and
    path in memory.
    """

    def __init__(self, initial_state, goal_state, agent_id):
        self.initial_state = initial_state
        self.current_state = initial_state
        self.goal_state = goal_state
        self.score = 0
        self.id = agent_id
        self.path = []
        self.i = 0

    def update_strategy(self, strategy):
        self.strategy = strategy

    def calculate_path(self, map):
        if (self.strategy == 'A*' or self.strategy == 'A* update every step' or
                self.strategy == 'A* update if collision in next step'):
            p = ProblemeGrid2D(self.current_state,
                               self.goal_state, map, 'manhattan')
            # print(probleme.astar(p))
            self.path = self.path[:self.i] + probleme.astar(p)[1:]
            # print(self.path)

    def update_position(self, map, playerStates, i):
        """Updates the position of the agent and if the goal is reached
        returns True """
        self.i = i  # change the current step

        # if the goal is reached end the game
        if (self.current_state == self.goal_state):
            print("le joueur " + str(self.id) + " with strategy = " +
                  self.strategy + " a atteint son but!")
            self.score += 1
            return True

        if (self.strategy == 'A*'):
            if i == 0:
                self.calculate_path(map)
            self.current_state = self.path[i]

        if (self.strategy == 'A* update every step'):
            self.calculate_path(map)
            self.current_state = self.path[i]

        if (self.strategy == 'A* update if collision in next step'):
            if i == 0:
                self.calculate_path(map)
            rowcol = self.path[i]
            dynamic_map = map.copy()
            while rowcol in playerStates.values():  # if there is collision in next step
                dynamic_map[rowcol] = False
                self.calculate_path(dynamic_map)
                rowcol = self.path[i]
                print(rowcol)
            self.current_state = rowcol

        playerStates[str(self.id)] = self.current_state
        return False
