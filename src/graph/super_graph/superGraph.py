from src.graph.lexical_graph.framenet import framenet_graph
from src.graph.lexical_graph.wordnet import wordnet_graph
from src.graph.lexical_graph.verbnet import verbnet_graph

from src.graph.ngram_graph.bigraph_new import document_graph
from src.graph.relatednessGraph.nltkGraph.relatedness_graph import RelatednessGraph
from src.graph.relatednessGraph.openIE_results.openIE import OpenInformationExtraction

class superGraph:

    def __init__(self,corpus):
        super(superGraph).__init__()
