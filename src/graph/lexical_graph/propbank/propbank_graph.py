'''
Provides information about the arguements of verbs.
Can be used in conjunction with VerbNet

'''


from nltk.corpus.reader import propbank
from src.graph.lexical_graph.base.base import Base

class propBank_graph(Base):

    def __init__(self,docpath):
        super(propBank_graph,self).__init__(docpath)
        self.PropReader = propbank.PropbankCorpusReader()

    def get_document_rolesets(self,docnum):
        return self.PropReader.roleset(self.corpus[docnum])

    def get_corpus_rolesets(self):
        return self.PropReader.roleset(' '.join(self.corpus))

    def get_document_verbs(self, docnum):
        return self.PropReader.verbs(self.corpus[docnum])

    def get_corpus_verbs(self):
        return self.PropReader.verbs(' '.join(self.corpus))

    def build_graph(self):
        return 0
