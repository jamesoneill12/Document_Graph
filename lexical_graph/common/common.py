from os import listdir
from os.path import isfile, join

class Common():
    def __init__(self,docpath="C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"):

        self.docpath = docpath
        self.filenames = [f for f in listdir(docpath) if isfile(join(docpath, f))]
        self.filepaths = [(docpath + f) for f in self.filenames]
        self.corpus = [open(docpath + f, mode='r').read() for f in self.filenames]

    def
