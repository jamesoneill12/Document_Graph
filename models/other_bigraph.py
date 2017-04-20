# highestweightednodes.py
# Author: Gungor Budak
# Requires Python 2.7.x and NetworkX 1.9.1
# How to run e.g. python highestweightednodes.py HPRD_PPI.txt output.txt 10
import sys
import networkx
from collections import OrderedDict
# Construct the network reading from the file
# file should have only two columns (of two nodes)
# with no header and it should be tab delimited
def constructNetwork(network_file):
	# Open the network file
	with open(network_file, "r") as network:
		# Empty graph
		G = networkx.Graph()
		# Each edge in the network
		for edge in network:
			# Strip and split edge
			nodes = edge.rstrip("\n").split("\t")
			# Add nodes to the graph
			G.add_edge(nodes[0], nodes[1])
	return G
# Compute clustering coefficient for each node in the network
def computeClusteringCoefficient(G, cores_sorted):
	# Calculate CC for each node
	for n, k in cores_sorted.iteritems():
		# Calculate CC, round and limit to two sig. figures
		cc = round(networkx.clustering(G, n), 2)
		# Update cores_sorted with CC values
		cores_sorted[n] = (k, cc)
	# k-core sorted dictionary is sorted by CC greater to smaller
	core_sorted_by_cc = OrderedDict(sorted(cores_sorted.iteritems(), key=lambda t: t[1], reverse=True))
	# Return the sorted dictionary
	return core_sorted_by_cc
# Write results to a table
def writeTable(output_file, node_number, core_sorted_by_cc):
	# Counter variable
	c = 0
	# Open output file
	with open(output_file, "w") as output:
		for n, (k, cc) in core_sorted_by_cc.iteritems():
			# Write the line
			output.write(str(n) +" "+ str(k) +" "+ str(cc) +"\n")
			# Increment the counter by 1
			c += 1
			# Break the loop when the counter becomes 10
			if c == node_number:
				break
# Main method
def main():
	# Get network file from the user
	network_file = sys.argv[1]
	# Get output file from the user
	output_file = sys.argv[2]
	# Get output number of nodes in the output file
	node_number = int(sys.argv[3])
	# Get the network
	network = constructNetwork(network_file)
	# Get cores
	cores = networkx.core_number(network)
	# Sort cores from greater to smaller
	cores_sorted = OrderedDict(sorted(cores.iteritems(), key=lambda t: t[1], reverse=True))
	# Get clustering coefficients computed
	core_sorted_by_cc = computeClusteringCoefficient(network, cores_sorted)
	# Write results to a table
	writeTable(output_file, node_number, core_sorted_by_cc)
# Run
main()