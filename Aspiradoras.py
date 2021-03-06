"""
Fecha de creación: 8 de noviembre del 2021
Equipo 3: 
Jorge Chávez Badillo				A01749448
Liam Garay Monroy				   A01750632
Ariadna Jocelyn Guzmán Jiménez 	 A01749373
Amy Murakami Tsutsumi 			   A01750185

Simulación de agentes (aspiradoras) que recorren una habitación y limpian las celdas sucias. Al final de la simulación se mostrará el tiempo necesario para que todas las celdas estén limpias, el porcentaje de celdas limpias al final de la simulación y el número de movimientos realizados por todos los agentes. Dado el tamaño de la habitación (MxN), el número de agentes, el porcentaje de celdas sucias y el tiempo máximo de ejecución.
"""

# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos varios agentes en la misma celda se usa MultiGrid para que se permita esta acción.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation


from mesa.datacollection import DataCollector

import pandas as pd 

import numpy as np

class Loseta(Agent):
    '''
    Representa un agente o una celda que tiene valor 0 si está limpia o 1 si está sucia
    '''
    def __init__(self, unique_id, model):
        '''
        Crea un agente con estado inicial 0 (celda limpia). También se define un nuevo estado cuyo valor será definido más adelante.
        '''
        super().__init__(unique_id, model)
        self.next_state = None
        self.sucia = 0

class Aspiradora(Agent):
    '''
    Representa a un agente o una celda que podrá moverse y limpiar en cada paso
    '''
    def __init__(self, unique_id, model):
        '''
        Crea un agente Aspiradora. También se define un nuevo estado cuyo valor será definido más adelante. 
        '''
        super().__init__(unique_id, model)
        self.next_state = None
        self.pasos = 0
        self.limpias = 0
    
    def step(self):
        '''
        Este método indica las acciones (moverse o limpiar) que realizará el agente en cada paso.
        '''
        self.move()
        self.limpia()
        self.pasos += 1
        
    

    def move(self):
        '''
        Este método define el movimiento que puede realizar el agente (cualquiera de las 8 celdas vecinas).
        '''
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def limpia(self):
        '''
        Este método cambia el valor de una loseta sucia a una limpia, es decir, de 1 a 0.
        '''
        
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        Loseta = cellmates[0]
        if(type(Loseta) != type(self)):
            if(Loseta.sucia == 1):
                Loseta.sucia = 0
                self.limpias += 1


    def advance(self):
        '''
        Define el nuevo estado calculado del método step.
        '''
        self.live = self.next_state
            
class AspirarModel(Model):
    '''
    Define el modelo del movimiento de las aspiradoras, declara las celdas como losetas
    limpias, así como define el porcentaje de las losetas sucias.
    '''
    def __init__(self, width, height):
        self.num_agents =  3569
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True #Para la visualizacion usando navegador
        #for (content, x, y) in self.grid.coord_iter():
        
        for (content, x, y) in self.grid.coord_iter():
            c = Loseta((x+2, y+2), self)
            self.grid.place_agent(c, (x, y))
            self.schedule.add(c)
        for i in range(self.num_agents):
            a = Aspiradora((1, i+1), self)
            self.grid.place_agent(a, (1, 1)) 
            self.schedule.add(a)

##
        
        porcentaje = 47
        area = self.grid.width*self.grid.height
        numLosetas = (area * porcentaje)//100
        print("Número de losetas:",numLosetas)
        print("Agentes totales:",self.schedule.get_agent_count())

        
        for i in range(numLosetas):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            c = self.grid[x][y]
            c[0].sucia=1
        
    
    def step(self):
        self.schedule.step()
        
