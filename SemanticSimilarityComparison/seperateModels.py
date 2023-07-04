# Import necessary libraries
import os
import spacy
import numpy as np
from gensim.models import Word2Vec
from gensim.corpora import Dictionary
from gensim.similarities import WmdSimilarity
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import pinecone as pc
from sentence_transformers import SentenceTransformer

# Define the models, similarity metrics, and storage methods
models = ['all-MiniLM-L6-v2', 'all-roberta-large-v1', 'word2vec']
similarity_metrics = ['cosine', 'euclidean', 'dotproduct']
storage_methods = ['pinecone', 'no_index']

# Define your choice of model, storage, and similarity metric
model_choice = 3  # Select between 1-3
storage_choice = 1  # Select between 1-2
similarity_choice = 2  # Select between 1-3

# Initialize the spacy tokenizer
spacy_tokenizer = spacy.load('en_core_web_sm')

# Load the corpus
with open('Barack_Obama.txt', 'r', encoding='utf8') as f:
    corpus = f.read()

# Split the corpus into sentences and tokenize them
corpus_sentences = [spacy_tokenizer(sentence).text.split() for sentence in corpus.split('.')]

# Define the query sentences and tokenize them
query_sentences = [spacy_tokenizer(sentence).text.split() for sentence in ['Obama speaks to the media in Illinois, Chicago']]

# Initialize the model
model_name = models[model_choice - 1]
if model_name == 'word2vec':
    # Use Gensim's Word2Vec for the 'word2vec' model
    model = Word2Vec(corpus_sentences, vector_size=100, window=5, min_count=1, workers=4)
    #Compute sentence embeddings by averaging word vectors
    corpus_embeddings = np.array([np.mean([model.wv[word] for word in sentence if word in model.wv and np.any(model.wv[word])] or [np.zeros(100)], axis=0) for sentence in corpus_sentences])
    query_embeddings = np.array([np.mean([model.wv[word] for word in sentence if word in model.wv and np.any(model.wv[word])] or [np.zeros(100)], axis=0) for sentence in query_sentences])
else:
    # Use SentenceTransformer for the other models
    model = SentenceTransformer(model_name)
    corpus_embeddings = model.encode([" ".join(sentence) for sentence in corpus_sentences])
    query_embeddings = model.encode([" ".join(sentence) for sentence in query_sentences])

# Initialize the storage method
storage_method = storage_methods[storage_choice - 1]
if storage_method == 'pinecone':
    pc.init(api_key="bfe6ce12-d327-4243-a7c0-e8a955e1b3b3", environment="us-west1-gcp-free")

    # Create a Pinecone index
    index_name = "semanticsimilaritycomparison"
    #sometimes after 1 run, comment the below line and run again. idk why but it works.
    pc.create_index(name=index_name, metric=similarity_metrics[similarity_choice - 1], dimension=corpus_embeddings.shape[1])

    # Initialize the index
    index = pc.Index(index_name=index_name)

    # Add the corpus embeddings to the Pinecone index
    item_ids = [str(i) for i in range(len(corpus_embeddings))]
    
    corpus_embeddings_list = [embedding.tolist() for embedding in corpus_embeddings]

    # Upsert vectors into the Pinecone index
    index.upsert(list(zip(item_ids, corpus_embeddings_list)))

# Initialize the similarity metric
similarity_metric = similarity_metrics[similarity_choice - 1]
try:
    # Calculate the similarity
    if similarity_metric == 'cosine':
        similarity = cosine_similarity(query_embeddings, corpus_embeddings)
    elif similarity_metric == 'euclidean':
        similarity = euclidean_distances(query_embeddings, corpus_embeddings)
    elif similarity_metric == 'dotproduct':
        similarity = np.dot(query_embeddings, corpus_embeddings.T)

    # If using Pinecone, query the index
    if storage_method == 'pinecone':
        for query_embedding in query_embeddings:
            results = index.query(query_embedding.tolist(), top_k=3)  # Converted to list
            # Print the results
            print(f"Model: {model_name}, Storage: {storage_method}, Similarity: {similarity_metric}")
            print(results)
            for match in results.matches:
                print(f"Matched sentence: {' '.join(corpus_sentences[int(match.id)])}, Score: {match.score}")

    # If not using Pinecone, print the top 3 most similar sentences for each query
    else:
        top_k = 3
        for i, query_embedding in enumerate(query_embeddings):
            print("Printing the local one")            
            top_k_indices = np.argsort(similarity[i])[-top_k:]
            top_k_similarities = similarity[i][top_k_indices]

            # Print the results
            print(f"Model: {model_name}, Storage: {storage_method}, Similarity: {similarity_metric}")
            for j in range(top_k):
                print(f"Matched sentence: {' '.join(corpus_sentences[top_k_indices[j]])}, Score: {top_k_similarities[j]}")

except Exception as e:
    print(f"An error occurred while calculating the {similarity_metric} similarity: {e}")

# If using Pinecone, delete the index after each run
#if storage_method == 'pinecone':
    #pc.deinit()
    #pc.delete_index(index_name)
