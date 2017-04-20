import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

relations = pd.read_csv("results.txt",sep='\t',names = ["Confidence", "Subject", "Predicate", "Object"])
graph = nx.DiGraph()
for i in range(relations.shape[0]):
    graph.add_node(relations['Subject'][i])
    graph.add_edge(relations['Subject'][i],relations['Predicate'][i])
    graph.add_node(relations['Object'][i])
    graph.add_edge(relations['Predicate'][i],relations['Object'][i])

index = nx.betweenness_centrality(graph)
plt.rc('figure', figsize=(12, 7))
pos = nx.spring_layout(graph)
nx.draw_networkx(graph, pos, edge_color='r', alpha=.3, linewidths=0)
plt.show()
