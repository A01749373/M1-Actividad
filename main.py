"""
Visualizador del Juego de la Vida
Esta parte es completamente diferente a la que hizo Edgar pues el lo hace todo en Jupyter
Octubre 8, 2021
"""

from Aspiradoras import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if(type(agent) == Aspiradora):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    if(type(agent) == loseta):
        if(agent.sucia == 1):
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey" #Grises pequeños al morir
            portrayal["Layer"] = 1
            portrayal["r"] = 0.1

    return portrayal

ancho = 50
alto = 25
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(GameLifeModel,
                       [grid],
                       "Trafic Model",
                       {"width":ancho, "height":alto})
server.port = 8521 # The default
server.launch()