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
        # BUG WENT AWAY WITH LIST AND MAP USE, UNUSED CODE
        # def in_bounds(pos):
        #     px, py = pos
        #     return 0 <= px < 49 and 0 <= py < 49
        #
        # x, y = self.pos

        neighbor_list = []  # stores all neighbors around the cell
        top_neighbors = ["", "", ""]  # stores the 3 neighbors over the cell

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

        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            neighbor_list.append(str(neighbor.condition))
        print(neighbor_list)

        # Assuming grid goes 1,2,3,4,5,6 from left top to right
        top_neighbors = [neighbor_list[2], neighbor_list[4], neighbor_list[7]]

        combined_states = "".join(top_neighbors)  # combined state string for top cells
        self._next_condition = state_result[combined_states]

        # DIDNT WORK, DO NOT USE
        # if (
        #     (left_condition is None and mid_condition == 1)
        #     or (
        #         left_condition == 1
        #         and mid_condition is None
        #         and right_condition is None
        #     )
        #     or (
        #         left_condition is None
        #         and mid_condition == 1
        #         and right_condition is None
        #     )
        # ):
        #     self._next_condition = 1
        # else:
        #     self._next_condition = 0

    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
