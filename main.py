from ngram_graph.bigram_graph import *
import json
from networkx.readwrite import json_graph

type = "bigram"
filenames,documents = get_local_docs()
kpe_textrank = get_doc_kpe(documents,filenames,type=type)
wg = WordGraph()
dG = [wg.textrank_document_graph(document,filenames=filename) for (document,filename) in zip(documents,filenames)]
data = [json_graph.node_link_data(dg) for dg in dG]

root_path = 'C:/xampp/htdocs/bigram_graph/'+type + '_docs/'

for filename in filenames:
    open(root_path+filename + '.json', 'w')

for graph,filename in zip(data,filenames):
    with open(root_path+filename+'.json', 'w') as f:
        json.dump(graph, f, indent=4)
