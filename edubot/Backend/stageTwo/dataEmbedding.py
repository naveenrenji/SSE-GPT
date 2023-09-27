import pinecone as pc
from sentence_transformers import SentenceTransformer
import spacy
import pickle
import os
from time import time

t = time()

# Load the sentence transformer model
model_name = 'sentence-transformers/all-roberta-large-v1'

# Function to save object
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# Function to load object
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Read the text file
with open('sseData.txt', 'r') as f:
    corpus = f.read()

# Tokenize the text into sentences
spacy_tokenizer = spacy.load('en_core_web_sm')
spacy_tokenizer.max_length = len(corpus)  # or some other large number
# doc = spacy_tokenizer(text)
corpus_sentences = [spacy_tokenizer(sentence).text.split() for sentence in corpus.split('.')]

model = SentenceTransformer(model_name)
corpus_embeddings = model.encode([" ".join(sentence) for sentence in corpus_sentences])

# # Initialize Pinecone
# pc.init(api_key="f8d808a1-f1a9-409e-b32b-f2fff6df629c", environment="us-west4-gcp-free")

# # Define the index name
# index_name = 'ssedata'

# # Create or connect to the Pinecone index
# if index_name not in pc.list_indexes():
#     pc.create_index(name=index_name, metric="cosine", dimension=len(corpus_embeddings[0]))

# index = pc.Index(index_name=index_name)

# # Add the corpus embeddings to the Pinecone index
# item_ids = [str(i) for i in range(len(corpus_embeddings))]

# corpus_embeddings_list = [embedding.tolist() for embedding in corpus_embeddings]

# # Upsert vectors into the Pinecone index
# index.upsert(list(zip(item_ids, corpus_embeddings_list)))

# Save tokenized sentences and embeddings
save_obj(corpus_sentences, 'corpus_sentences')
save_obj(corpus_embeddings, 'corpus_embeddings')

def get_model_and_index():
    return model, corpus_sentences, corpus_embeddings

get_model_and_index()

print('Time to generate embeddings of corpus:', round(time() - t, 4), 'seconds')
