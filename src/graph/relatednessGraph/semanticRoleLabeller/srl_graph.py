from practnlptools.tools import Annotator
from textblob import TextBlob
from pattern.text import en
from src.graph.lexical_graph.base.base import Base
import json
from nltk.corpus import stopwords

#from nltk.corpus import stopwords
#text1 = "It is obligatory that the Bank of Ireland transfer asset to customer, that requests the asset"
# print annotator.getAnnotations(text1)['verbs']
#print annotator.getAnnotations(text)['verbs']
#print annotator.getAnnotations(text1)['srl']
#print annotator.getAnnotations(text)['srl']

class srlGraph(Base):

    def __init__(self,docpath):
        super(srlGraph,self).__init__(docpath)
        self.stopwords = stopwords.words("english")
        self.annotator = Annotator()

    def srl_corpus_extraction(self, stopwords=None):

        sem_rl = self.annotator.getAnnotations(self.corpus, dep_parse=True)['srl']
        srl_corpus = [self.annotator.getAnnotations(doc)['srl'] for doc in self.corpus]
        return srl_corpus

    def srl_document_extraction(self, document_id=0, stopwords=None):
        return self.annotator.getAnnotations(self.corpus[document_id], dep_parse=True)['srl']

    def get_doc_canon(self,document_id):
        sem_rl = self.annotator.getAnnotations(self.corpus[document_id], dep_parse=True)['srl']
        canon = [en.singularize(word) for word in str(TextBlob(sem_rl[0]['C-A1'])).split()
                 if word not in stopwords]

        blob = TextBlob(sem_rl[0]['A1'])
        nounPhrases = blob.noun_phrases.singularize()
        sr_verb_concept = self.annotator.getAnnotations(sem_rl[0]['A1'])['srl']

        concat_noun_concepts = set(sum([word.split() for word in nounPhrases], []))
        predicates = list(set(canon) - concat_noun_concepts)

        return canon

def main():
    filename = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"
    srlg = srlGraph(filename)
    print (srlg.srl_document_extraction(document_id=10))

main()







