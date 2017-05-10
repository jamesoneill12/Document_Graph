import re, os
from nltk.stem import WordNetLemmatizer
import numpy as np
from nltk.corpus import stopwords
from collections import defaultdict
from gensim import models, corpora
from os.path import isfile
from os import listdir
import matplotlib.pyplot as plt
# https://www.archives.gov/open/dataset-cfr.html#how - open usa gov data

flatten = lambda l: [item for sublist in l for item in sublist]

def flattener(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

def cleaner(string):
    string = re.sub(r"[^A-Za-z0-9(),!?\'`]", ' ', string)
    string = re.sub(r'\([^)]\)', ' ', string)
    string = re.sub(r"\'s", ' ', string)
    string = re.sub(r"\'ve", ' ', string)
    string = re.sub(r"n\'t", ' ', string)
    string = re.sub(r"\'re", ' ', string)
    string = re.sub(r"\'d", ' ', string)
    string = re.sub(r"\'ll", ' ', string)
    string = re.sub(r"^,", ' ', string)
    string = re.sub(r"!", ' ', string)
    string = re.sub(r"\?", ' ', string)
    string = re.sub(r"\s{2,3}", ' ', string)
    string = re.sub(r",", ' ', string)
    string = re.sub(r'\([^)]\)', ' ', string)
    string = re.sub(r'\(', ' ', string)
    string = re.sub(r'\)', ' ', string)
    string = re.sub(r'section', ' ', string)
    string = re.sub(r'sub', ' ', string)
    string = re.sub(r'subsection', ' ', string)
    string = re.sub(r'paragraph', ' ', string)
    string = re.sub(r'i{2,3}', ' ', string)
    return string

def get_clean_corpus(filenames):
    vectorizer = text.CountVectorizer(input='filename', stop_words='english', min_df=20, decode_error='ignore')
    dtm = vectorizer.fit_transform(filenames).toarray()
    vocab = np.array(vectorizer.get_feature_names())
    lmtzr = WordNetLemmatizer()  # create a lemmatizer object
    corpus = [
        [lmtzr.lemmatize(word) for word in cleaner(open(filename, mode="r", encoding="utf8").read().lower()).split() if
         not word in stopwords.words('english')] for filename in filenames]
    return (corpus)

def get_types(corpus_by_type):
    clean_splits = defaultdict()
    for (types, v) in corpus_by_type.items():
        if len(v.keys()) > 0:
            try:
                clean_splits[types] = get_clean_corpus(list(v.keys()))
            except:
                pass
    return (clean_splits)

# split on types within the readpath
def split_on_type(readpath='C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/recent_uk_docs/2016/'):

    leg_types = ['anaw', 'asp', 'nia', 'nisi', 'nisr', 'ssi', 'ukci', 'ukcm', 'ukla', 'ukpga', 'uksi', 'wsi', 'ssi']
    type_counts = [0] * len(leg_types)
    filenames = list(flattener([(readpath + f) for f in listdir(readpath) if 'welsh-data' not in f]))
    corpus_count = dict(zip(leg_types, type_counts))
    corpus_by_type = defaultdict()

    for filename in filenames:
        for (i, s) in enumerate(leg_types):
            if s in filename:
                if corpus_count[s] == 0:
                    corpus_by_type[s] = {filename: corpus_count[s]}
                else:
                    corpus_by_type[s].update({filename: corpus_count[s]})
                corpus_count[s] += 1
    clean_splits = get_types(corpus_by_type)
    return (clean_splits)

def corpus_retriever(readpath=os.getcwd() + '\\data\\results\\'):
    if 'uk' in readpath and '20' not in readpath:
        filepaths = [(readpath + f + '/') for f in listdir(readpath)]
        filenames = flatten(
            [[(filepath + f) for f in listdir(filepath) if 'welsh-data' not in f] for filepath in filepaths])
    elif 'uk' in readpath and '/20/' in readpath:
        filenames = [(readpath + f) for f in listdir(readpath)]
    else:
        filenames = [readpath + f for f in listdir(readpath) if isfile(join(readpath, f))]

    vectorizer = text.CountVectorizer(input='filename', stop_words='english', min_df=20, decode_error='ignore')
    dtm = vectorizer.fit_transform(filenames).toarray()
    vocab = np.array(vectorizer.get_feature_names())
    lmtzr = WordNetLemmatizer()  # create a lemmatizer object
    corpus = [[lmtzr.lemmatize(word) for word in cleaner(open(filename, mode="r", encoding="utf8").read()).split() if
               not word in stopwords.words('english')] for filename in filenames]

    # stopwords = Counter(chain.from_iterable(texts)).most_common(300)
    # corpus  = [list(set(texts[i]) - set(stopwords)) for i,line in enumerate(texts)]
    return (vocab, corpus)

def make_lda(corpus, n_topics=10, save=True, source=''):
    dictionary = corpora.Dictionary(corpus)
    corpus = [dictionary.doc2bow(text) for text in corpus]
    ldamodel = models.ldamodel.LdaModel(corpus,
                                        num_topics=n_topics,
                                        id2word=dictionary,
                                        passes=10,
                                        alpha='auto',
                                        eval_every=5)
    if save:
        ldamodel.save(source + "_LDAModel.model")
    return ldamodel

def load_lda(show=False, n_topics=10, source=''):
    # print dictionary, corpus
    # ldavis.prepare(lda, corpus, dictionary)
    ldamodel = models.ldamodel.LdaModel.load(source + '_LDAModel.model')
    if show:
        print(ldamodel.print_topics(num_topics=10))
    terms = ldamodel.show_topics(num_topics=n_topics)
    return (ldamodel, terms)


def get_matches(uk_terms):
    matches = []
    for term in uk_terms:
        matches.append(re.findall(r'\"(.+?)\"', term[1]))
    return matches


def get_matches_from_topics(uk_model, ntops=10):
    matches = []
    for term in uk_model.show_topics(num_topics=ntops):
        matches.append(re.findall(r'\"(.+?)\"', term[1]))
    return matches


def plot_topics(x_sne, X, matches, title='t-SNE Words of UK legislation', savename=None, figdim=(10, 7)):
    plt.rc('figure', figsize=figdim)
    plt.rc('font', size=10)
    plt.rc('lines', linewidth=4)
    plt.rc('axes', color_cycle=('#377eb8', '#e41a1c', '#4daf4a',
                                '#984ea3', '#ff7f00', '#ffff33'))
    if savename != None:
        for i in range(x_sne.shape[0]):
            plt.scatter(x_sne[i, 0], x_sne[i, 1], alpha=.5)
            plt.text(x_sne[i, 0], x_sne[i, 1], s=' ' + str(i))

        # 't-SNE Manifold Topics of EUROVOC Journals'
        plt.title(title)
        plt.savefig("pca_topic")
        plt.close()
        plt.figure()

    for i, n in enumerate(X.get_feature_names()):
        try:
            plt.scatter(x_sne[i, 0], x_sne[i, 1], alpha=.5)
            # or x_sne[i, 0], x_sne[i, 1]x_sne1[i], x_sne2[i]
            print(str(i) + ' : ' + ' '.join(matches[i]))
            plt.text(x_sne[i, 0], x_sne[i, 1], s=str(i) + ' : ' + ' '.join(matches[i]), fontsize=10)
        except:
            pass

    plt.title(title)
    plt.savefig(savename)
    plt.show()

    plt.close()
