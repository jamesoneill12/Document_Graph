
from networkx.readwrite import json_graph
from  src.graph.ngram_graph.bigram_graph import *
from src.graph.relatednessGraph.coreference.coreference_graph import coreferenceGraph

filename = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"
cr_g = coreferenceGraph(filename)

#syn, anto = wg.get_corpus_syns(antonyms=True)
#print (syn)

cr_g.get_coreferences()

