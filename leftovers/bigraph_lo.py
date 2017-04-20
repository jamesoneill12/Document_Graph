#simpleNetworkx(dG)
'''
#first compute the best partition
partition = community.best_partition(dG)
size = float(len(set(partition.values())))
pos = nx.spring_layout(dG)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(dG, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))

nx.draw_networkx_edges(dG,pos, alpha=0.5)
plt.show()
'''