from mesa.visualization import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

from model import GameOfLife

# Colors for living and dead cells
COLORS = {1: "#000000", 0: "#AAAAAA"}


# The portrayal is a dictionary that is used by the visualization server to
# generate a visualization of the given agent.
def GoL_portrayal(entityCell):
    if entityCell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = entityCell.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[entityCell.condition]

    return portrayal


# The canvas element will be 500x500 pixels, with each cell being 5x5 pixels.
# The portrayal method will fill each cell with a representation of the entityCell
# that is in that cell.
canvas_element = CanvasGrid(GoL_portrayal, 50, 50, 500, 500)

# The chart will plot the number of each type of entityCell over time.
entityCell_chart = ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)


# The model parameters will be set by sliders controlling the initial density
model_params = {
    "height": 50,
    "width": 50,
    "density": Slider("Cell density", 0.65, 0.01, 1.0, 0.01),
}

# The modular server is a special visualization server that allows multiple
# elements to be displayed simultaneously, and for each of them to be updated
# when the user interacts with them.
server = ModularServer(
    GameOfLife, [canvas_element, entityCell_chart], "Game Of Life", model_params
)

server.launch()
