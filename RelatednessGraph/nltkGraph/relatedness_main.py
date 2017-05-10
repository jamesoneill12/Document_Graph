from relatedness_graph import *
from relatedness_test import draw_network
from semanticNetwork import Semantic_Network

# entities = list of terms
entities = []
# connections = list of tuples ("term1","term2", value)
connections = []

sg = Semantic_Network()
sg.add_entities(entities)
sg.add_connections(connections)

draw_network(sg,location="C:\Users\1\James\Research\Projects\GraphProject"
                         "\LegalGraph\Legal_Graph_Words\Implementation"
                         "\images\\relatedness_graph")

document_entities = get_entities()
