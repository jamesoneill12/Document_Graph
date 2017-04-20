import string
from sys import maxsize
import matplotlib.pyplot as plt
import networkx as nx
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from helpers import *
import community
import numpy as np

#  for the community stuff - https://bitbucket.org/taynaud/python-louvain/issues/15/directed-graphs
# community example - http://perso.crans.org/aynaud/communities/index.html
#from NetworkxD3 import simpleNetworkx

class WordGraph():

    def __init__(self):
        self.dG = nx.DiGraph()

    def textrank_document_graph(self,documents,filenames, save_image=False,print_graph_info=False):
        dG = self.dG
        stop = set(stopwords.words('english'))
        wordList1 = documents.split(None)
        wordList2 = [string.rstrip(WordNetLemmatizer().lemmatize(clean_str((x.lower()),together=True)), ',.!?;') for x in wordList1 if x not in stop]
        # IF USING NER
        #document_entities = [NERTag(document.split()) for document in wordList2]
        if filenames:
            kpe_textrank = get_doc_kpe(documents, filenames, type="textrank",format="list")

        kpe_textrank_words = [kpe[0] for kpe in kpe_textrank]
        kpe_textrank_scores = [kpe[1] for kpe in kpe_textrank]
        dG = self.construct_graph(dG,kpe_textrank_words,kpe_textrank_scores)
        dG = self.get_communities(dG)
        if print_graph_info:
            self.get_graph_info()
        if save_image:
            print (dG.nodes(data=True))
            plt.show()
            nx.draw(dG, width=2, with_labels=True)
            plt.savefig("images/bigram_graph.png")
        return dG

    def bigram_document_graph(self,documents,filenames,save_image=False):
        dG = self.dG
        stop = set(stopwords.words('english'))
        wordList1 = documents.split(None)
        wordList2 = [string.rstrip(WordNetLemmatizer().lemmatize(clean_str((x.lower()),together=True)),
                                   ',.!?;') for x in wordList1 if x not in stop]
        if filenames:
            kpe_textrank = get_doc_kpe(documents, filenames, type="textrank",format="list")
        dG = self.construct_graph(dG,wordList2)
        dG = self.get_communities(dG)
        return dG

    def get_communities(self,dG):
        # community detection
        parts = community.best_partition(self.dG.to_undirected())
        values = [parts.get(node) for node in self.dG.nodes()]
        # k-core and clustering co-efficient - self loops here ?
        # cores = nx.core_number(dG)
        for i, word in enumerate(self.dG.nodes()):
            self.dG.node[word]['group'] = values[i]
            # dG.node[word]['kcore'] = cores[i]
            self.dG.node[word]['cc'] = nx.clustering(self.dG.to_undirected(), word)

    def get_graph_info(self):
        for node in self.dG.nodes():
            print ('%s:%d\n' % (node, self.dG.node[node]['count']))
        for edge in self.dG.edges():
            print ('%s:%d\n' % (edge, maxsize - self.dG.edge[edge[0]][edge[1]]['weight']))

    def construct_graph(self,dG,words,scores=None):
        if scores is None:
            scores = np.ones((len(dG.nodes()),), dtype=np.float)
        for i, word in enumerate(words):
            try:
                next_word = words[i + 1]
                if not dG.has_node(word):
                    dG.add_node(word)
                    dG.node[word]['count'] = scores[i]
                else:
                    dG.node[word]['count'] += scores[i]
                if not dG.has_node(next_word):
                    dG.add_node(next_word)
                    dG.node[next_word]['count'] = 0
                if not dG.has_edge(word, next_word):
                    dG.add_edge(word, next_word, weight=maxsize - scores[i])
                else:
                    dG.edge[word][next_word]['weight'] -= scores[i]
            except IndexError:
                if not dG.has_node(word):
                    dG.add_node(word)
                    dG.node[word]['count'] = scores[i]
                else:
                    dG.node[word]['count'] += scores[i]
            except:
                raise

