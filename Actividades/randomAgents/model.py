from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import RandomAgent, ObstacleAgent, TrashAgent, ChargingStation

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        M: Number of trash in the simulation
        O: Number of obstacles
        height, width: The size of the grid to model
    """
    def __init__(self, N, M, O, width, height):
        self.num_agents = N
        self.num_trash = M
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0})


        # random obstacle positions 
        obs_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # place obstacles on the grid
        for i in range(O):
            obs = ObstacleAgent(i+1000, self)
            self.schedule.add(obs)
            pos = obs_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = obs_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(obs, pos)


        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):

            a = RandomAgent(i+1000, self) 
            self.schedule.add(a)

            b = ChargingStation(i+1000, self)
            self.schedule.add(b)

            pos = pos_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(a, pos)
            self.grid.place_agent(b, pos)

        # Generate random trash positions
        trash_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        for i in range(self.num_trash):
            t = TrashAgent(i+1000, self)
            self.schedule.add(t)

            pos = trash_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(t, pos)

        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)

        
