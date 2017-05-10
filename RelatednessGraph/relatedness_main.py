from relatedness_graph import *
from relatedness_test import draw_graph,draw_network
import os
dog_entities = ["dog", "cat", "horse", "saddle", "rider", "mouse", "cheese",
                "churning", "milk", "cow", "human", "race", "gambling"]
dog_connections = [("dog", "cat", 50),
                    ("dog", "horse", 10),
                    ("horse", "saddle", 60),
                    ("horse", "rider", 30),
                    ("rider", "saddle", 40),
                    ("horse", "race", 30),
                    ("rider", "race", 35),
                    ("dog", "race", 20),
                    ("cat", "mouse", 50),
                    ("race", "gambling", 40),
                    ("mouse", "cheese", 50),
                    ("cheese", "milk", 60),
                    ("milk", "cow", 60),
                    ("cheese", "cow", 30),
                    ("rider", "human", 50),
                    ("milk", "churning", 20),
                    ("human", "gambling", 30)]
'''
sg = Semantic_Network()
sg.add_entities(dog_entities)
sg.add_connections(dog_connections)
draw_network(sg,location="C:/Users/1/James/Research/Projects/Graph Project/"
                         "Legal_Graph_Words/Implementation/RelatednessGraph/"
                         "relatedness_graph.png")
'''
document_entities = get_entities()
