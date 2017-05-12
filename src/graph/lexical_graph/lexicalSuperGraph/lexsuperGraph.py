from src.graph.lexical_graph.framenet.framenet_graph import framenetGraph
from src.graph.lexical_graph.wordnet.wordnet_graph import wordnetGraph
from src.graph.lexical_graph.verbnet.verbnet_graph import verbnetGraph
import networkx as nx

class lexsuperGraph(wordnetGraph,verbnetGraph,framenetGraph):

    def __init__(self,doclist):

        super(self,doclist).__init__()
        self.lexGraph = nx.MultiGraph(self.w)
        self.superGraph = self.combineGraphs()

    def combineGraphs(self):

        first = nx.compose(wordnetGraph,verbnetGraph,'lexSuperGraph')
        second = nx.compose(wordnetGraph,framenetGraph,'lexSuperGraph')
        super = nx.compose()
        return super
