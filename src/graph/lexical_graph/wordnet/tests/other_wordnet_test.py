from src.graph.lexical_graph.wordnet.wordnet_graph import wordnetGraph
from src.graph.lexical_graph.wordnet.other_wordnet_graph import wnGraph

filename = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"
wng = wnGraph(filename)
wng.graph

#wg = wordnetGraph(filename)
#syn, anto = wg.get_corpus_syns(antonyms=True)
#print (syn)
#wg.create_wordnetDocGraph(save_pic=True)
