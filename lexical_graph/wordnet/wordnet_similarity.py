from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()

# Computing English word similarity using Li method
wns.word_similarity('dog', 'cat', 'li') # 0.449327301063
# Computing Spanish word similarity using Lin method
wns.monol_word_similarity('perro', 'gato', 'spa', 'lin') #0.876800984373
# Computing Chinese word similarity using Wu & Palmer method
wns.monol_word_similarity('狗', '猫', 'cmn', 'wup') # 0.857142857143
# Computing Spanish and English word similarity using Resnik method
wns.crossl_word_similarity('perro', 'cat', 'spa', 'eng', 'res') #7.91166650904
# Computing Spanish and Chinese word similarity using Jiang & Conrad method
wns.crossl_word_similarity('perro', '猫', 'spa', 'cmn', 'jcn') #0.31023804699
# Computing Chinese and English word similarity using WPath method
wns.crossl_word_similarity('狗', 'cat', 'cmn', 'eng', 'wpath')#0.593666388463

