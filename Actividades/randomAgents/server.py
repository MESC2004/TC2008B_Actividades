import mesa

from model import RandomModel, ObstacleAgent, TrashAgent, ChargingStation, RandomAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer


def agent_portrayal(agent):
    colors = ["red", "brown", "cyan", "grey", "yellow"]
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, RandomAgent)):
        portrayal["Color"] = colors[agent.unique_id % 5]
        portrayal["Layer"] = 3
        portrayal["r"] = 0.5
        portrayal["text"] = f"{agent.energy}%"
        portrayal["text_color"] = "black"


    if (isinstance(agent, ObstacleAgent)):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1

    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2 
        portrayal["r"] = 0.35

    if (isinstance(agent, ChargingStation)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7

    return portrayal

model_params = {
        "N": mesa.visualization.Slider("Roombas", 5, 1, 15),
        "M": mesa.visualization.Slider("Trash", value=0.1, min_value=0, max_value=1, step=0.05),
        "O": mesa.visualization.Slider("Obstacles", value=0.1, min_value=0, max_value=1, step=0.05),
        "width": 20,
        "height": 20
}
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", model_params)
                       
server.port = 8523 # The default
server.launch()
