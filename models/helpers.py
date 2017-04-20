import re
from os import listdir
from os.path import isfile, join
import nltk
from nltk.stem.snowball import SnowballStemmer
import keyphrase_extractor
from nltk.tag.stanford import StanfordNERTagger
import os

'''
# only for use with python 3
def spacy_ner(text):
    import spacy
    nlp = spacy.load('en')
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.label_, ent.text)
        # GPE London
        # GPE United Kingdom
'''

def NERTag(text):
    os.environ['CLASSPATH'] = "C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar"
    os.environ['STANFORD_MODELS'] = "C:/Users/1/James/stanford-parser-full-2015-12-09"
    os.environ['JAVAHOME'] = "C:/Program Files/Java/jdk1.8.0_102"
    ner = StanfordNERTagger('C:/Users/1/James/stanford-ner-2015-12-09/classifiers/'
                            'english.all.3class.distsim.crf.ser.gz',
                   'C:/Users/1/James/stanford-ner-2015-12-09/stanford-ner.jar')
    r= ner.tag(text)
    return r

def tokenize_and_stem(text):
    stemmer = SnowballStemmer("english")
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    #stems = [stemmer.stem(t) for t in filtered_tokens]
    stems = [t for t in filtered_tokens]

    return stems

def clean_str(string,together=False):

    string = re.sub(r"[^A-Za-z0-9(),!?\'`]", " ", string)
    string = re.sub(r"[0-9]", " ",string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r"^,", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    if together is True:
        return string.lower()
    else:
        return string.lower().split()

def get_local_docs(which='all'):
    docs = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"
    filenames = [f for f in listdir(docs) if isfile(join(docs, f))]
    filepaths = [(docs+f) for f in filenames]
    documents = []
    for f in filepaths:
        with open(f, 'r') as myfile:
            data = clean_str(myfile.read().replace('', ''),together=True)
        documents.append(data)
    if which is 'all':
        filenames = [f.replace(".txt","")
                         .replace(".csv","")
                         .replace("."," ")
                         .replace("_"," ")
                         .title() for f in filenames]
        return filenames,documents
    else:
        return documents

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def get_doc_kpe(documents, filenames, type = 'chunks', format="dict"):

    if format is "list":
        doc_candidates = keyphrase_extractor.score_keyphrases_by_textrank(documents)
    else:
        doc_candidates = {}
        for doc,name in zip(documents,filenames):
            if type == 'chunks':
                doc_candidates[name] = keyphrase_extractor.extract_candidate_chunks(doc)
            elif type == 'words':
                doc_candidates[name] = keyphrase_extractor.extract_candidate_words(doc)
            elif type == 'tfidf':
                doc_candidates[name] = keyphrase_extractor.score_keyphrases_by_tfidf(doc)
            elif type == 'textrank':
                doc_candidates[name] = keyphrase_extractor.score_keyphrases_by_textrank(doc)
    return doc_candidates
