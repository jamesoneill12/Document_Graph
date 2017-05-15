import networkx as nx
import matplotlib.pyplot as plt
from src.graph.lexical_graph.wordnet.other_wordnet_graph import wnGraph
from src.graph.ngram_graph.bigram_graph import WordGraph
from src.graph.lexical_graph.framenet.framenet_graph import framenetGraph
from src.graph.lexical_graph.verbnet.verbnet_graph import verbnetGraph

class CombineGraphs():

    def __init__(self,graph_pair):
        self.graph1 = graph_pair[0]
        self.graph2 = graph_pair[1]

    def combine_wordnetNgram(docpath="C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"):

        # wordnet graph
        wg = wnGraph(docpath)
        wn_graph = wg.graph
        wg.degree_distribution()

        # bigram graph
        bigraph = WordGraph(docpath)
        ngram_g = bigraph.textrank_document_graph(save_image=True)

        # combine and display
        combine = nx.compose(wn_graph, ngram_g)
        # return the graph and labels
        nx.draw(combine,with_labels=True)  # ,with_labels=True)
        plt.show()

        return combine

    def combine_wordnetVerbNet(docpath="C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"):
        # wordnet graph
        wg = wnGraph(docpath)
        wn_graph = wg.graph

        # bigram graph
        vg = verbnetGraph(docpath)


        # combine and display
        combine = nx.compose(wn_graph, ngram_g)
        # return the graph and labels
        nx.draw(combine, with_labels=True)  # ,with_labels=True)
        plt.show()

        return combine





