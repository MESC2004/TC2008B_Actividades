
from mesa import Agent
import heapq

class RandomAgent(Agent):
    """
    Agent that moves randomly and returns to its charging station when necessary.
    Attributes:
        unique_id: Agent's ID
        steps_taken: Number of steps taken by the agent
        energy: Energy level of the agent (0 - 100)
        home: Position of the agent's charging station
        returning_home: Flag to indicate if the agent is returning to the charging station
        visited_cells: Set of cells visited by the agent and their neighbors
        path_home: List of positions representing the path back to the charging station
    """
    def __init__(self, unique_id, model, energy=100):
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.energy = energy
        self.home = None
        self.returning_home = False
        self.visited_cells = set()
        self.path_home = []

    def heuristic(self, a, b):
        """
        Heuristic function for A* (Manhattan distance) or staircase distance to home.
        """
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, start, goal):
        # G4G A* info and algorithm: https://www.geeksforgeeks.org/a-search-algorithm-in-python/
        """
        Perform A* search from start to goal.
        start: current position when calculating the path
        goal: charging station to reach
        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        # g_score is the cost of the cheapest path from start to the current cell
        g_score = {start: 0}
        # f_score is the sum of g_score and the heuristic function (Manhattan distance)
        f_score = {start: self.heuristic(start, goal)}
        visited = set()

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                return self.reconstruct_path(came_from, current)

            visited.add(current)
            neighbors = self.model.grid.get_neighborhood(current, moore=True, include_center=False)

            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                # Check if neighbor is a free cell (not an obstacle)
                cell_contents = self.model.grid.get_cell_list_contents(neighbor)
                if any(isinstance(obj, ObstacleAgent) for obj in cell_contents):
                    continue  # Skip obstacles

                tentative_g_score = g_score[current] + 1  # movement energy cost is 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        """
        Reconstruct the path from start to goal.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def move_randomly(self):
        """
        Moves the agent to a random free neighboring cell.
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        free_spaces = []
        for pos in possible_steps:
            # Get the contents of each cell in the neighborhood
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            has_obstacle = any(isinstance(obj, ObstacleAgent) for obj in cell_contents)
            has_agent = any(isinstance(obj, RandomAgent) for obj in cell_contents)
            # If there is no obstacle and no agent in the cell, add it to the list
            if not has_obstacle and not has_agent:
                free_spaces.append(pos)

        if free_spaces:
            # Record the current position and its neighbors
            self.visited_cells.add(self.pos)
            self.visited_cells.update(possible_steps)

            # Move to a random free space
            next_move = self.random.choice(free_spaces)
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
            self.energy -= 1
        else:
            # No possible moves, stay in the same place
            pass

    def move(self):
        """ 
        Determines the next move for the agent. If there is trash in the neighborhood, it moves to the trash,
        if not, it moves randomly. 
        Also checks for collisions with other agents and obstacles.
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        # Search for trash in the neighborhood
        trash_cells = []
        for pos in possible_steps:
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            if any(isinstance(obj, TrashAgent) for obj in cell_contents):
                has_agent = any(isinstance(obj, RandomAgent) for obj in cell_contents)
                if not has_agent:
                    trash_cells.append(pos)

        if trash_cells:
            # Record the current position and its neighbors
            self.visited_cells.add(self.pos)
            self.visited_cells.update(possible_steps)

            # Move to the trash
            next_move = self.random.choice(trash_cells)
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
            self.energy -= 1
        else:
            # Move randomly
            self.move_randomly()

    def step(self):
        """ 
        Agent's behavior at each step.
        """
        if self.energy <= 0:
            # Agent has no energy; stop acting
            return

        # If the agent's home position is not set, set it now
        if self.home is None:
            self.home = self.pos

        # Check if the agent needs to return home
        distance_to_home = self.heuristic(self.pos, self.home)
        buffer = 5  # Extra energy units as buffer
        if not self.returning_home and self.energy <= distance_to_home + buffer:
            # Start returning home
            self.returning_home = True
            self.path_home = self.a_star_search(self.pos, self.home)
            if self.path_home is None:
                # No path found, cannot return home
                self.returning_home = False
                self.path_home = []
                return

        if self.returning_home:
            if self.pos == self.home:
                # Agent has reached home, recharge
                if self.energy < 100:
                    self.energy = min(self.energy + 5, 100)  # Recharge 5% per step
                else:
                    # Fully charged, resume normal behavior
                    self.returning_home = False
                    self.path_home = []
                return  # Stay on the charging station
            else:
                # Follow the path home
                if len(self.path_home) > 1:
                    next_move = self.path_home[1]  # Next position in the path
                    # Check if next_move is accessible
                    cell_contents = self.model.grid.get_cell_list_contents(next_move)
                    if any(isinstance(obj, ObstacleAgent) for obj in cell_contents):
                        # Path is blocked, need to recalculate
                        self.path_home = self.a_star_search(self.pos, self.home)
                        if self.path_home is None:
                            # No path found, cannot return home
                            self.returning_home = False
                            self.path_home = []
                            return
                        else:
                            next_move = self.path_home[1]
                    # Move to next cell
                    self.model.grid.move_agent(self, next_move)
                    self.path_home = self.path_home[1:]
                    self.steps_taken += 1
                    self.energy -= 1
                else:
                    # Path exhausted but not at home
                    self.returning_home = False
                    self.path_home = []
        else:
            # Normal behavior
            cell_contents = self.model.grid.get_cell_list_contents([self.pos])
            trash = [obj for obj in cell_contents if isinstance(obj, TrashAgent)]

            if trash:
                # Record the current position and its neighbors
                possible_steps = self.model.grid.get_neighborhood(
                    self.pos,
                    moore=True,
                    include_center=False
                )
                self.visited_cells.add(self.pos)
                self.visited_cells.update(possible_steps)

                # Remove the trash
                self.model.grid.remove_agent(trash[0])
                self.model.schedule.remove(trash[0])
                self.steps_taken += 1
                self.energy -= 1
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
    Agent that acts as trash on the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class ChargingStation(Agent):
    """
    Agent that acts as a charging station on the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

