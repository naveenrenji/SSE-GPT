'''
This script uses word2vec to encode the text to be used as a "knowledge base"
and then calculates the semantic distance between given sentences, based on the "knowledge base".

The source text is from wikipedia.
'''

# importing the required libraries
from gensim.models import Word2Vec
import wikipedia
from datetime import datetime
import multiprocessing
from time import time
import numpy as np
from sklearn.decomposition import PCA
from matplotlib import pyplot


def txt_clean(word_list, min_len, stopwords_list):
    """
    Performs a basic cleaning to a list of words.

    :param word_list: list of words
    :type: list
    :param min_len: minimum length of a word to be acceptable
    :type: integer
    :param stopwords_list: list of stopwords
    :type: list
    :return: clean_words list of clean words
    :type: lists

    """
    clean_words = []
    for line in word_list:
        parts = line.strip().split()
        for word in parts:
            word_l = word.lower().strip()
            if word_l.isalpha():
                if len(word_l) > min_len:
                    if word_l not in stopwords_list:
                        clean_words.append(word_l)
                    else:
                        continue

    return clean_words


'''
----------- Main
'''


# loading the stopwords and setting the minimum length for the words
stp_file = 'stopwords_en.txt'
stopwords_file = open(stp_file,'r', encoding='utf8')

# initializing the list of stopwords
stopwords_list = []

# populating the list of stopwords and the list of words from the text file
for word in stopwords_file:
    stopwords_list.append(word.strip())

word_min_len = 2

# printing starting time
start_time = datetime.now()
print ('\n-Starting the embedding process at {}'.format(start_time), '\n')

# reading a corpus from Wikipedia and loading it into a list
wikipedia.set_lang("en")
topic = "Barack_Obama"
corpus = wikipedia.page(topic).content.strip().replace('\n\n\n','\n').replace('\n\n','\n').replace('\n','#').replace('(','').replace(')','')
# creating a list from the corpus
#   it is a list of strings composed by words to be cleaned
#   each string is a "phrase"
corpus_lst = corpus.split("#")

# creating a list of lists of cleaned words
#   each list is a "phrase"
corpus_lst_lst = []
for elem in corpus_lst:
    clean_elem = txt_clean(elem.split(), word_min_len, stopwords_list)
    corpus_lst_lst.append(clean_elem)

# setting the parameters for Word2Vec
cores = multiprocessing.cpu_count()
t = time()

# defining the parameters for the model
w2vec_model = Word2Vec(min_count=5, window=6, vector_size=300, sample=1e-5, alpha=0.5, negative=11, workers=cores-1)
# building the vocabulary for the model
w2vec_model.build_vocab(corpus_lst_lst)
# training the model
w2vec_model.train(corpus_lst_lst, total_examples=w2vec_model.corpus_count, epochs=60)

print('Time to develop and train the model: {} mins'.format(round((time() - t) / 60, 4)))

# extracting labels (that are the words in the vocabulary) and vectors from the model as numpy arrays
labels = np.asarray(w2vec_model.wv.index_to_key)
vectors = np.asarray(w2vec_model.wv.vectors)
print('\nNumber of words in the vocabulary:', len(labels))
print ('Number of sentences:', w2vec_model.corpus_count)
#print ('\n This is the list of labels in the model:\n', labels)
#print ('\n and this is the list of the related vectors:\n', vectors)

'''
# the following is to represent the model as PCA
pca = PCA(n_components=2)
result = pca.fit_transform(vectors)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(w2vec_model.wv.index_to_key)
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
'''

# the following are the sentences we want to compare
query_sentences = ['Obama speaks to the media in Illinois', 'The president greets the press in Chicago',
                   'The hawk flies high in the sky']

# cleaning the sentences
clean_queries = []
for step in range (0, len(query_sentences)):
    sentence_clean = txt_clean(query_sentences[step].split(), word_min_len, stopwords_list)
    clean_queries.append(sentence_clean)

# calculating and printing the Word Mover’s Distance (WMD) between the 1 sentence and the others
#   based on the "knowledge base" in the word2vec model
'''
WMD is based on the idea of finding the minimum “traveling distance” between documents, that is
  the most efficient way to “move” the words distribution of document 1 to the words distribution of document 2
  check here: http://vene.ro/blog/word-movers-distance-in-python.html
  The original paper is here: http://proceedings.mlr.press/v37/kusnerb15.pdf

  The implementation in Gensim uses pyemd, a Python wrapper for the earth mover’s distance
'''
for iter in range (1, len(clean_queries)):
    distance = w2vec_model.wv.wmdistance(clean_queries[0], clean_queries[iter])
    print('\nDistance between the sentence --', query_sentences[0], '-- and --', query_sentences[iter], '-- is:')
    print('   ', distance)

