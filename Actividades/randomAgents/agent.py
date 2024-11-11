from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0



    def move_randomly(self):
        """
        Random movement function for the cleaner agents, also checks if anothjer agent already
        took a cell that the random agent wants to move to. THis avoids the slim chance of 
        collisions between agents when moving randomly
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        free_spaces = []
        for pos in possible_steps:
            # get the contents of each cell in the neighborhood
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            has_obstacle = any(isinstance(obj, ObstacleAgent) for obj in cell_contents)
            has_agent = any(isinstance(obj, RandomAgent) for obj in cell_contents)
            # if there is no obstacle and no agent in the cell, add it to the list
            if not has_obstacle and not has_agent:
                free_spaces.append(pos)

        if free_spaces:
            # if there are free spaces, move to a random one
            next_move = self.random.choice(free_spaces)
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
        else:
            # no possible moves, stay in the same place, do not spend energy (TODO), do not increment steps
            pass

    
    def move(self):
        """ 
        Determines the next move for the agent. If there is trash in the neighborhood, it moves to the trash. 
        Also checks for collisions with other agents and obstacles.
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        # search for trash in the neighborhood and add to list if exists
        trash_cells = []
        for pos in possible_steps:
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            if any(isinstance(obj, TrashAgent) for obj in cell_contents):
                # is there an agent already in the scheduler?
                has_agent = any(isinstance(obj, RandomAgent) for obj in cell_contents)
                if not has_agent:
                    # trash has not been "claimed", add to the list
                    trash_cells.append(pos)

        if trash_cells:
            # Move to trash
            next_move = self.random.choice(trash_cells)
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
        else:
            # move randomly as final (topmost) option
            self.move_randomly()

    
    def step(self):
        """ 
        Verifica si hay basura en la posición actual; si es así, la limpia, si no, se mueve.
        """
        # Verificar si hay basura en la posición actual
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        trash = [obj for obj in cell_contents if isinstance(obj, TrashAgent)]

        if trash:
            # Limpiar la basura
            self.model.grid.remove_agent(trash[0])
            self.model.schedule.remove(trash[0])
            self.steps_taken += 1
        else:
            self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  


class TrashAgent(Agent):
    """
    Agent that acts as trash on the grid
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class ChargingStation(Agent):
    """
    Agent that acts as charging station on the grid
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        pass
