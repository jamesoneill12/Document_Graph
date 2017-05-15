import networkx as nx
from nltk.corpus import wordnet as wn
from  src.graph.lexical_graph.base.base import Base
import matplotlib.pyplot as plt
from collections import Counter

def wordnet_graph(words):

    """
     Construct a semantic graph and labels for a set of object categories using
     WordNet and NetworkX.

     Parameters:
     ----------
          words : set
         Set of words for all the categories.

     Returns:
     -------
     graph : graph
         Graph object containing edges and nodes for the network.
     labels : dict
         Dictionary of all synset labels.
     """

    graph = nx.DiGraph()
    labels = {}
    seen = set()

    def recurse(s):

        """ Recursively move up semantic hierarchy and add nodes / edges """

        if not s in seen:                               # if not seen...
            seen.add(s)                                 # add to seen
            graph.add_node(s.name)                      # add node
            labels[s.name] = s.name().split(".")[0]     # add label
            hypernyms = s.hypernyms()                   # get hypernyms

            pattern = r'method'

            for s1 in hypernyms:                        # for hypernyms
                #m = re.search(pattern, s1.name)
                #print(m.group())
                #print(s1.name)
                graph.add_node(s1.name)                 # add node
                graph.add_edge(s.name, s1.name)         # add edge between
                recurse(s1)                             # do so until top

    # build network containing all categories
    for word in words.split():                          # for all categories
        try:
            s = wn.synset(str(word) + str('.n.01'))         # create synset
            recurse(s)                                      # call recurse
        except:
            pass

    # return the graph and labels
    nx.draw(graph) # ,with_labels=True)
    plt.show()

    return graph , labels

class wnGraph(Base):

    def __init__(self,docpath):

        super(wnGraph,self).__init__(docpath)
        self.graph, self.labels = wordnet_graph(self.corpus[0])
        self.degree = self.graph.degree()

    def get_shortest_path(self, n1,n2):
        self.shortest_path = nx.shortest_path(self.graph, n1, n2)

    def get_betweenness(self, n1, n2):
        self.betweenness = nx.shortest_path(self.graph, n1, n2)

    def get_closeness(self, n1, n2):
        self.closeness = nx.closeness_centrality(self.graph, n1, n2)

    def get_eigen(self, n1, n2):
        self.eigen_centrality = nx.eigenvector_centrality(self.graph, n1, n2)

    def degree_distribution(self):

        #in_hist = [self.degree.values(x) for x in sorted(set(self.degree))]
        counts = sorted(set(Counter(self.degree.values())))
        plt.figure()
        plt.plot(sorted(set(self.degree.values())),'ro-')

        # out-degree
        plt.legend(['In-degree','Out-degree'])
        plt.xlabel('Degree')
        plt.ylabel('Number of nodes')
        plt.title('Degree of exapanded wordnet terms for randomly sampled corpus document')
        plt.show()

        plt.savefig('degree_distribution.pdf')
        plt.close()




