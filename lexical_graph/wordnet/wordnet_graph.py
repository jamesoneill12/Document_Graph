from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

print (wn.synsets('good'))

car = wn.synset('regulation')
print ("HYPERNYMS")
print (car.hypernyms())
print ("HYPONYMS")
print (car.hyponyms())

synonyms = []
antonyms = []

for syn in wn.synsets("good"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))
print (syn.lemmas())

w1 = wn.synset('regulation.n.01')
w2 = wn.synset('regulation.n.01')
print(w1.wup_similarity(w2))

from textblob import Word

word = Word("regulation")
print (word.synsets[:5])
print (word.definitions[:5])

word = Word("regulation")
for syn in word.synsets:
    for l in syn.lemma_names():
        synonyms.append(l)

G = nx.Graph()

w = word.synsets[1]

G.add_node(w.name())
for h in w.hypernyms():
    print (h)
    G.add_node(h.name())
    G.add_edge(w.name(), h.name())

for h in w.hyponyms():
    print (h)
    G.add_node(h.name())
    G.add_edge(w.name(), h.name())

print (G.nodes(data=True))
plt.show()
nx.draw(G, width=2, with_labels=True)
plt.savefig("path.png")
