# MIGUEL SORIA A01028033
# OCT 30 2024
# Cell script for game of life

from mesa import Agent


class EntityCell(Agent):
    """ """

    def __init__(self, pos, model):
        """
        Create a new Entity Cell.

        Args:
            pos: The entity's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = 0
        self._next_condition = None

    def step(self):
        joined_top = "   "  # string to save the combined 3 top cells
        x, y = self.pos  # self coords

        # Result map from game rules
        state_result = {
            "111": 0,
            "110": 1,
            "101": 0,
            "100": 1,
            "011": 1,
            "010": 0,
            "001": 1,
            "000": 0,
        }

        # Boundary check
        if (
            self.pos[0] < self.model.grid.width - 1
            and self.pos[0] > 0
            and self.pos[1] != 49
        ):
            # gets top neighbors and saves their conditions in an array
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                neigh_x, neigh_y = neighbor.pos  # neighbor coords
                if neigh_y == y + 1:
                    if neigh_x == x - 1:
                        # replace values from base string
                        joined_top = joined_top.replace(
                            joined_top[0], str(neighbor.condition), 1
                        )
                    elif neigh_x == x:
                        joined_top = joined_top.replace(
                            joined_top[1], str(neighbor.condition), 1
                        )
                    elif neigh_x == x + 1:
                        joined_top = joined_top.replace(
                            joined_top[2], str(neighbor.condition), 1
                        )

            # check resulting string in map
            self._next_condition = state_result[joined_top]

    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
