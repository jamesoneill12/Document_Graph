'''
I have to decide how the wiktionary graph is incorporated.
In other words, by what criteria do we expand corpus words to
incorporating related

'''

from src.graph.lexical_graph.base.base import Base
from wiktionaryparser import WiktionaryParser
from collections import defaultdict
from sys import maxsize
import networkx as nx
import numpy as np
import json


class wiktionaryGraph(Base):

    def __init__(self,docpath,language='english'):

        super(wiktionaryGraph, self).__init__(docpath)

        self.parser = WiktionaryParser()
        self.parser.set_default_language(language)

        self.wiki_parse = defaultdict()
        self.pronounciations = defaultdict()
        self.definitions = defaultdict()
        self.etymologies = defaultdict()

        # still undecided whether the graph in general should have multiple links
        # or if it should be one link with multiple inputs.

        self.wikiGraph = nx.MultiGraph()

    def print_test(self,word='test'):
        test_word = self.parser.fetch(word)
        return test_word

    def get_corpus_wiktionary(self,instance='definitions'):

        for (id,document) in enumerate(self.corpus):
            for word in set(document.split()):
                try:
                    self.wiki_parse[id] = dict(word = self.parser.fetch(word))
                except:
                    pass

        return self.wiki_parse

    def get_document_wiktionary(self,doc_id,instance='definitions'):

        doc_def = defaultdict()
        for word in set(self.corpus[doc_id].split()):
            try:
                doc_def[word] = self.parser.fetch(word)
            except:
                pass

        return doc_def

    def build_wiktionary_graph(self,scores=None):

        if scores is None:
            scores = np.ones((len(self.wikiGraph.nodes()),), dtype=np.float)

        for document in self.corpus:
            for i, word in enumerate(document.split()):

                try:
                    next_word = document[i + 1]

                    if not self.wikiGraph.has_node(word):
                        self.wikiGraph.add_node(word)
                        self.wikiGraph.node[word]['count'] = scores[i]
                    else:
                        self.wikiGraph.node[word]['count'] += scores[i]

                    if not self.wikiGraph.has_node(next_word):
                        self.wikiGraph.add_node(next_word)
                        self.wikiGraph.node[next_word]['count'] = 0
                    if not self.wikiGraph.has_edge(word, next_word):
                        self.wikiGraph.add_edge(word, next_word, weight=maxsize - scores[i])
                    else:
                        self.wikiGraph.edge[word][next_word]['weight'] -= scores[i]

                except IndexError:
                    if not self.wikiGraph.has_node(word):
                        self.wikiGraph.add_node(word)
                        self.wikiGraph.node[word]['count'] = scores[i]
                    else:
                        self.wikiGraph.node[word]['count'] += scores[i]
                except:
                    raise



wiki_g = wiktionaryGraph("C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/")
out = wiki_g.print_test()
#for rw in out[0]['definitions']:
    #print(rw['relatedWords'])
