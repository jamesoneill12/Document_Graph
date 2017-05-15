from nltk.corpus.reader import verbnet as vn
import networkx as nx
import matplotlib.pyplot as plt
from src.graph.lexical_graph.base.base import Base

def verbnet_graph(words):

    graph = nx.Graph()
    labels = {}
    seen = set()

    def recurse(s):

        """ Recursively move up semantic hierarchy and add nodes / edges """

        if not s in seen:                               # if not seen...
            seen.add(s)                                 # add to seen
            graph.add_node(s.name)                      # add node
            labels[s.name] = s.name().split(".")[0]     # add label
            hypernyms = s.hypernyms()                   # get hypernyms

            pattern = r'"([A-Za-z0-9_\./\\-]*)"'

            for s1 in hypernyms:                        # for hypernyms
                #m = re.search(pattern, s1.name)
                #print(m.group())
                graph.add_node(s1.name)                 # add node
                graph.add_edge(s.name, s1.name)         # add edge between
                recurse(s1)                             # do so until top

    # build network containing all categories
    for word in words.split():                          # for all categories
        try:
            s = vn.classids(str(word))         # create synset
            recurse(s)                                      # call recurse
        except:
            pass

    # return the graph and labels

    nx.draw(graph,with_labels=True)
    plt.show()

    return graph , labels

class vnGraph(Base):

    def __init__(self,docpath):

        super(vnGraph,self).__init__(docpath)
        self.graph, self.labels = verbnetGraph(self.corpus[0])
