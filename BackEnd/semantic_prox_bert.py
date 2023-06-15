from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initializing the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Reading in the corpus
with open('Barack_Obama.txt', 'r', encoding='utf8') as f:
    corpus = f.read()

# Splitting the corpus into sentences
corpus_sentences = corpus.split('.')

# Getting the embeddings for the corpus
corpus_embeddings = model.encode(corpus_sentences)

# Defining the query sentences
query_sentences = ['Obama speaks to the media in Illinois', 'The president greets the press in Chicago']

# Getting the embeddings for the query sentences
query_embeddings = model.encode(query_sentences)

# Calculate the cosine similarity between the query sentences
similarity = cosine_similarity(query_embeddings[0].reshape(1, -1), query_embeddings[1].reshape(1, -1))
print(f"Cosine similarity between '{query_sentences[0]}' and '{query_sentences[1]}' is: ", similarity[0][0])
