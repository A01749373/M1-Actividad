"""
Fecha de creación: 8 de noviembre del 2021
Equipo 3: 
Jorge Chávez Badillo				A01749448
Liam Garay Monroy				   A01750632
Ariadna Jocelyn Guzmán Jiménez 	 A01749373
Amy Murakami Tsutsumi 			   A01750185
"""

from Aspiradoras import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

listaLosetasLimpias = []
def agent_portrayal(agent):
    '''
    Permite visualizar a los agentes dependiendo de su tipo y su estado
    '''

    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if(type(agent) == Aspiradora):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        if(agent.pasos == 20):
            #losetasLimpias = agent.limpias
            #print("Losetas limpias después de 20 pasos: ", losetasLimpias)
            listaLosetasLimpias.append(agent.limpias)
            #print(max(listaLosetasLimpias))
            
    if(type(agent) == Loseta):
        if(agent.sucia == 1):
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey" #Grises limpios desde el principio
            portrayal["Layer"] = 1
            portrayal["r"] = 0.1
    
    return portrayal


ancho = 50
alto = 25
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(AspirarModel,
                       [grid],
                       "Trafic Model",
                       {"width":ancho, "height":alto})


server.port = 8521 # The default
server.launch()
