'''
Author - James O' Neill

Description -

This is the final supergraph that should combine all lexical, ngram and relatedness intermediate graphs
into the final supergraph. This can only cope with small corpuses no larger than 50 documents of reasonable
size until the code is optimized.

I need to added more parallel computing to perform faster graph construction on all graph levels.

'''

from src.graph.lexical_graph.lexicalSuperGraph import lexsuperGraph
from src.graph.ngram_graph.bigram_graph import WordGraph
from src.graph.relatednessGraph.mitie.mikie_graph import mikieGraph


from src.graph.ngram_graph.bigraph_new import document_graph
from src.graph.relatednessGraph.nltkGraph.relatedness_graph import RelatednessGraph
from src.graph.relatednessGraph.openIE_results.openIE import OpenInformationExtraction

class superGraph():

    def __init__(self,corpus):
        super(superGraph).__init__()
