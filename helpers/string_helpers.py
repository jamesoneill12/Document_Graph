from nltk.stem import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import re

def tokenize_and_stem(text,tofile=False):

    amend_path = "C:/Users/1/James/Research/Projects/" \
                 "Publishing_Projects/Legal_Retrieval/" \
                 "data/amend_data/"

    stemmer = SnowballStemmer("english")
    wn = WordNetLemmatizer()

    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    print("Beginning tokenization ....")
    tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    stems = []

    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    print("Beginning lemmatization ...")
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            stems.append(wn.lemmatize(token))

    if tofile:
        print("Writing amendment data ...")
        with open(amend_path+"amendment_data", 'w') as file:
            for line in stems:
                file.writelines(' '.join(line))

    return stems

def clean_str(string):

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
    return string
