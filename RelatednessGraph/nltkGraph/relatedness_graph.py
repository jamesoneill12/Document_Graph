import networkx as nx
import os, nltk, re
from nltk.tag import StanfordNERTagger
from os import listdir
from os.path import isfile, join
import multiprocessing
from joblib import Parallel, delayed


def get_decaying_subgraph(graph, start_nodes, max_hops=3, decay_rate=0.5):
    """ Constructs a decaying subgraph centered on all of the nodes in iterable start_nodes.
    """
    subgraph = nx.Graph()
    subgraph.add_nodes_from(start_nodes)
    seen_node_set = set()
    hop_node_set = set(start_nodes)
    next_hop_set = set()
    for hop in range(max_hops):
        decay_multiplier = decay_rate ** hop
        for node in hop_node_set:
            for neighbor in graph.neighbors(node):
                if subgraph.has_edge(node, neighbor):
                    continue
                next_hop_set.add(neighbor)
                decayed_capacity = (decay_multiplier *
                                    graph[node][neighbor]['capacity'])
                subgraph.add_edge(node, neighbor, capacity=decayed_capacity)
            seen_node_set.add(node)
        hop_node_set = next_hop_set - seen_node_set
        next_hop_set.clear()
    return subgraph

def get_capacity_dict(graph):
    capacity_dict = dict()
    for edge in graph.edges():
        capacity_dict[edge] = graph.get_edge_data(*edge)['capacity']
    return capacity_dict

def get_entities(docs=None):

    ner = StanfordNERTagger(
        'C:/Users/1/James/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
        'C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar')

    if docs == None:
        docs = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"

    filenames = [f for f in listdir(docs) if isfile(join(docs, f))]
    filepaths = [(docs + f) for f in filenames]
    documents = {}
    document = []

    for (fname, f) in zip(filenames, filepaths):
        with open(f, 'r') as myfile:
            text = myfile.readlines()
        tags = ner.tag(text)

        for (word, tag) in tags:
            if tag != 'O':
                document.append(word)
        documents[remove_extenstion(fname).title()] = set(document)
    return documents

def remove_extenstion(f):
    return f.replace(".txt", "")\
        .replace(".csv", "")\
        .replace(".", " ")\
        .replace("_", " ")

def doc_rel(myfile,f):
    IN = re.compile(r'.*\bin\b(?!\b.+ing)')
    relations = []
    print(myfile)
    with open(f, 'r') as myfile:
        text = myfile.read()
        for rel in nltk.sem.extract_rels('ORGANIZATION', 'ORGANIZATION', text):
            relations.append(nltk.sem.rtuple(rel))
    return (relations)

def doc_ents(filename, f):
    ner = StanfordNERTagger(
        'C:/Users/1/James/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
        'C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar')

    document = []
    dd = {}
    with open(f, 'r') as myfile:
        text = myfile.readlines()

    for i, (word, tag) in enumerate(ner.tag(text)):
        if tag != 'O':
            document.append(word)
    dd[remove_extenstion(filename).title()] = set(document)
    return dd

class RelatednessGraph():

    def __init__(self,filenames='',filepaths=''):

        self.filenames = filenames
        self.filepaths = filepaths
        self.num_cores = multiprocessing.cpu_count() - 1

        os.environ['CLASSPATH'] = "C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar"
        os.environ['STANFORD_MODELS'] = "C:/Users/1/James/stanford-parser-full-2015-12-09"
        os.environ['JAVAHOME'] = "C:/Program Files/Java/jdk1.8.0_102"

    def get_decaying_subgraph(graph, start_nodes, max_hops=3, decay_rate=0.5):
        """ Constructs a decaying subgraph centered on all of the nodes in iterable start_nodes.
        """
        subgraph = nx.Graph()
        subgraph.add_nodes_from(start_nodes)
        seen_node_set = set()
        hop_node_set = set(start_nodes)
        next_hop_set = set()
        for hop in range(max_hops):
            decay_multiplier = decay_rate ** hop
            for node in hop_node_set:
                for neighbor in graph.neighbors(node):
                    if subgraph.has_edge(node, neighbor):
                        continue
                    next_hop_set.add(neighbor)
                    decayed_capacity = (decay_multiplier *
                                        graph[node][neighbor]['capacity'])
                    subgraph.add_edge(node, neighbor, capacity=decayed_capacity)
                seen_node_set.add(node)
            hop_node_set = next_hop_set - seen_node_set
            next_hop_set.clear()
        return subgraph

    def get_entities(self,docs=None):

        if docs == None:
            docs = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"

        filenames = [f for f in listdir(docs) if isfile(join(docs, f))]
        filepaths = [(docs+f) for f in filenames]
        documents = {} ; document = []

        for (fname,f) in zip(filenames,filepaths):
            with open(f, 'r') as myfile:
                text = myfile.readlines()
            tags = self.ner.tag(text)

            for (word,tag) in tags:
                if tag != 'O':
                    document.append(word)
            documents[remove_extenstion(fname).title()] = set(document)
        return documents

    def get_entities(self):
        return Parallel(n_jobs=self.num_cores)(delayed(doc_ents)(fname, f) for (fname, f) in zip(self.filenames, self.filepaths))

    def get_relations(self):
        return Parallel(n_jobs=self.num_cores)(delayed(doc_rel)(fname, f) for (fname, f) in zip(self.filenames, self.filepaths))

    def get_capacity_dict(self,graph):

        capacity_dict = dict()
        for edge in graph.edges():
            capacity_dict[edge] = graph.get_edge_data(*edge)['capacity']

        return capacity_dict

if __name__ == '__main__':

    docs = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"
    filenames = [f for f in listdir(docs) if isfile(join(docs, f))]
    filepaths = [(docs + f) for f in filenames]

    rg = RelatednessGraph(filenames,filepaths)
    entities = rg.get_entities()
    relations = rg.get_relations()
    print (relations)
