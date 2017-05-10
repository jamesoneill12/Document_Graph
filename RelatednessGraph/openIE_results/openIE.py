# coding: latin1
from os import listdir
from os.path import isfile, join
from subprocess import Popen,call
import nltk, csv
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import re
from networkx.drawing.nx_agraph import write_dot

class OpenInformationExtraction:

    def openfile(self,f,type="ollie"):
        if type is "ollie":
            with open(f, 'r') as a:
                s = nltk.PorterStemmer()
                l = nltk.WordNetLemmatizer()
                a = a.readlines()
                #a = a.readlines()  # a will equal 'soc, 32\nsoc, 1\n...' in your example#
                b = [l.lemmatize(x.lower()) for x in a if '\xef\xbb\xbf' not in x]
                return b

        elif type is "stanford":
            with open(f, 'r') as a:
                s = nltk.PorterStemmer()
                l = nltk.WordNetLemmatizer()
                lines = a.readlines()  # a will equal 'soc, 32\nsoc, 1\n...' in your example#
                ie = [line.lower().split("  ") for line in lines]
                return lines

    def clean_str(self,string):
        string = re.sub(r"[^A-Za-z,!?\`]", " ", string)
        string = re.sub(r"xe ","",string)
        string = re.sub(r"^,", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"    "," ",string)
        string = re.sub(r"       ", " ", string)
        string = re.sub(r"  "," ",string)
        #string = re.sub(r"^c[A-Z]",r"[A-Z]",string)
        #string = re.sub(r"\s{2,}", " ", string)
        string = re.sub(r'\b\w\b', ' ', string)
        return string

    def run(self,filenum=7,results=False,path="C:/Users/1/James/grctc/GRCTC_Project/"
                                              "Classification/Data/docs/",graph_name=None):
        self.graph_name = graph_name
        texts = []
        documents = {}
        document = []
        filenames = [f for f in listdir(path) if isfile(join(path, f))]
        filepaths = [(path + f) for f in filenames]
        text = self.clean_str(open(filepaths[filenum],'rb').read().strip())
        grctc_input_stanford = open('ie_sentence.txt', 'w')
        text = str(text).split(".")
        [grctc_input_stanford.write("%s\n" % t) for t in text]
        grctc_input_stanford.close()
        sb = Popen("run_stanfordIE.bat")
        stdout, stderr = sb.communicate()
        stanford_file = self.openfile("results.txt", type="stanford")
        file = str(stanford_file).replace("\\t", " ").split()
        if results:
            with open("results.txt", 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    print (row)

    def oie_graph(self):
        relations = pd.read_csv("results.txt",sep='\t',names = ["Confidence", "Subject", "Predicate", "Object"])
        graph = nx.MultiDiGraph()

        for i in range(relations.shape[0]):
            graph.add_node(relations['Subject'][i])
            graph.add_edge(relations['Subject'][i],relations['Predicate'][i])
            graph.add_node(relations['Object'][i])
            graph.add_edge(relations['Predicate'][i],relations['Object'][i])

        index = nx.betweenness_centrality(graph)
        plt.rc('figure', figsize=(12, 7))
        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos, edge_color='r', alpha=.3, linewidths=0)
        if self.graph_name !=None:
            nx.write_graphml(graph, self.graph_name+".graphml")
        plt.show()
        return graph

if __name__ == "__main__":
    oie = OpenInformationExtraction()
    oie.run(filenum=20,graph_name='example')
    graph = oie.oie_graph()
