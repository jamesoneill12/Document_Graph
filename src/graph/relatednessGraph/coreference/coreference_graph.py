'''
Why use co-reference resolution in a compositional graph ?
Information about

Anaphora: 'it' follows what is being co-referenced
Cataphora: 'it' precedes the co-refererred
Split antecedents: 'they' refers to two things, such as two people
Coreferring noun phrases:
'''


from src.graph.lexical_graph.base.base import Base
import networkx as nx
import os, nltk, re
from nltk.tag import StanfordNERTagger
from os import listdir
from os.path import isfile, join
import multiprocessing
from joblib import Parallel, delayed

def remove_extenstion(f):
    return f.replace(".txt", "")\
        .replace(".csv", "")\
        .replace(".", " ")\
        .replace("_", " ")

class coreferenceGraph(Base):

    def __init__(self,docpath):
        super(coreferenceGraph,self).__init__(docpath)

        self.ner_document_tags = []
        self.ner_document_coreferences = []

        self.ner_corpus_tags = []
        self.ner_corpus_coreferences = []

    def get_ner_corpus_tags(self):

        ner = StanfordNERTagger(
            'C:/Users/1/James/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
            'C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar')

        for document in self.corpus:
            for line in document:
                tags = ner.tag(' '.join(line))
                document = []
                for (word, tag) in tags:

                    if tag != 'O':
                        self.ner_corpus_tags.append(document.append(word))
        return self.ner_corpus_tags

    def get_ner_document_tags(self,document_id):

        ner = StanfordNERTagger(
            'C:/Users/1/James/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
            'C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar')

        for document in self.corpus[document_id]:
            for line in document:
                tags = ner.tag(' '.join(line))
                document = []
                for (word, tag) in tags:
                    if tag != 'O':
                        self.ner_corpus_tags.append(document.append(word))
        return self.ner_document_tags

    def get_coref_corpus(self):

        for document in self.corpus:
            for line in document:
                tags = ner.tag(' '.join(line))
                document = []
                for (word, tag) in tags:

                    if tag != 'O':
                        self.ner_corpus_tags.append(document.append(word))
        return self.ner_corpus_tags

    def get_coref_document(self, document_id):

        for document in self.corpus[document_id]:
            for line in document:
                tags = ner.tag(' '.join(line))
                document = []
                for (word, tag) in tags:
                    if tag != 'O':
                        self.ner_corpus_tags.append(document.append(word))

        return self.ner_document_tags

    # this function should get the index position in a document for each corefence
    def get_coref_position_pairs(self):
        return 0


