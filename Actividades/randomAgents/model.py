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
        M: Density of trash (value between 0 and 1)
        O: Density of obstacles (value between 0 and 1)
        height, width: The size of the grid to model
    """

    def __init__(self, N, M, O, width, height):
        super().__init__()  # Call the parent class's __init__ method
        self.num_agents = N
        self.num_trash = M
        self.grid = MultiGrid(width, height, torus=False) 

        self.schedule = RandomActivation(self)
        self.running = True 

        self.accumulated_steps = 0  # for setting a runtime limit

        self.datacollector = DataCollector( 
            model_reporters={
                "CleanCells": lambda m: m.count_clean_cells(),
                "DirtyCells": lambda m: m.count_dirty_cells(),
                "Time": lambda m: m.accumulated_steps,
            },
            agent_reporters={
                "Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0,
                "Battery": lambda a: a.energy if isinstance(a, RandomAgent) else None
            }
        )

        # Place obstacles on the grid based on obstacle density value "O"
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < O:
                obs = ObstacleAgent(self.next_id(), self)
                self.grid.place_agent(obs, (x, y))
                self.schedule.add(obs)            

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Add the agents and charging stations to random empty grid cells
        for i in range(self.num_agents):
            # Create agent
            a = RandomAgent(self.next_id(), self, 100) 
            self.schedule.add(a)

            # Create charging station
            b = ChargingStation(self.next_id(), self)
            self.schedule.add(b)

            pos = pos_gen(self.grid.width, self.grid.height)
            while not self.grid.is_cell_empty(pos):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(a, pos)
            self.grid.place_agent(b, pos)

        # Generate trash based on trash density value "M"
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < M and self.grid.is_cell_empty((x, y)):
                trash = TrashAgent(self.next_id(), self)
                self.grid.place_agent(trash, (x, y))
                self.schedule.add(trash)
        
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
        self.accumulated_steps += 1

        # Check if all trash is cleaned
        if self.count_dirty_cells() == 0:
            self.running = False

        # Stop the model after 250 steps
        if self.accumulated_steps >= 250:
            self.running = False

    def count_dirty_cells(self):
        return sum(1 for agent in self.schedule.agents if isinstance(agent, TrashAgent))

    def count_clean_cells(self):
        total_cells = self.grid.width * self.grid.height
        dirty_cells = self.count_dirty_cells()
        return total_cells - dirty_cells
       
