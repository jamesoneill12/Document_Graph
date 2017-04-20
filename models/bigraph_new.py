import string
from sys import maxsize
import matplotlib.pyplot as plt
import networkx as nx
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from models.helpers import *

#from NetworkxD3 import simpleNetworkx
def make_graph(text,scores=None):
    dG = nx.DiGraph()
    for i, word in enumerate(text):
        try:
            next_word = text[i + 1]
            if not dG.has_node(word):
                dG.add_node(word)
                if scores:
                    dG.node[word]['count'] = scores[i]
                else:
                    dG.node[word]['count'] = 1
            else:
                if scores:
                    dG.node[word]['count'] += scores[i]
                else:
                    dG.node[word]['count'] += 1
            if not dG.has_node(next_word):
                dG.add_node(next_word)
                dG.node[next_word]['count'] = 0

            if not dG.has_edge(word, next_word):
                if scores:
                    dG.add_edge(word, next_word, weight=maxsize - scores[i])
                else:
                    dG.add_edge(word, next_word, weight=maxsize - 1)
            else:
                if scores:
                    dG.edge[word][next_word]['weight'] -= scores[i]
                else:
                    dG.edge[word][next_word]['weight'] -= 1
        except IndexError:
            if not dG.has_node(word):
                dG.add_node(word)
                if scores:
                    dG.node[word]['count'] = scores[i]
                else:
                    dG.node[word]['count'] = 1
            else:
                if scores:
                    dG.node[word]['count'] += scores[i]
                else:
                    dG.node[word]['count'] += 1
        except:
            raise
        return dG

def document_graph(documents, save_image=False,graph_type='bigram',print_graph_info=False,filenames=None):
    stop = set(stopwords.words('english'))
    wordList1 = documents.split(None)
    wordList2 = [string.rstrip(WordNetLemmatizer().lemmatize(clean_str((x.lower()),together=True)), ',.!?;') for x in wordList1 if x not in stop]
    #document_entities = [NERTag(document.split()) for document in wordList2]
    if filenames:
        kpe_textrank = get_doc_kpe(documents, filenames, type="textrank",format="list")
    if graph_type is 'textrank':
        kpe_textrank_words = [kpe[0] for kpe in kpe_textrank]
        kpe_textrank_scores = [kpe[1] for kpe in kpe_textrank]
        #wordList2 = [[kpe,wl2] for kpe,wl2 in zip(kpe_textrank_words,wordList2)]
        dG = make_graph(kpe_textrank_words,scores=kpe_textrank_scores)
    elif graph_type is 'bigram':
        dG = make_graph(wordList2)
    if print_graph_info:
        for node in dG.nodes():
            print ('%s:%d\n' % (node, dG.node[node]['count']))
        for edge in dG.edges():
            print ('%s:%d\n' % (edge, maxsize - dG.edge[edge[0]][edge[1]]['weight']))
    if save_image:
        print (dG.nodes(data=True))
        plt.show()
        nx.draw(dG, width=2, with_labels=True)
        plt.savefig("images/bigram_graph.png")
    return dG
