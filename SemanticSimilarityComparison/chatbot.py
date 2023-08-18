import os
import spacy
import numpy as np
import pinecone as pc
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

# Define the models
model_name = 'sentence-transformers/all-roberta-large-v1'

# Initialize the spacy tokenizer
spacy_tokenizer = spacy.load('en_core_web_sm')

# Use SentenceTransformer for the model
model = SentenceTransformer(model_name)

# Initialize Pinecone
pc.init(api_key="bfe6ce12-d327-4243-a7c0-e8a955e1b3b3", environment="us-west1-gcp-free")

# Create a Pinecone index
index_name = "ssegpt"

# Check if the index already exists
existing_indexes = pc.list_indexes()
corpus_sentences = [] # Define corpus_sentences here
txt_file = open("Barack_Obama.txt","r", encoding='utf8')
txt_content = []
for t_line in txt_file:
    if t_line != '\n':
        txt_content.append(t_line)

# tokenizing by sentence the input text
corpus_sentences = []
for line in txt_content:
    doc = spacy_tokenizer(line)
    for sent in doc.sents:
        corpus_sentences.append(sent.text)

if index_name not in existing_indexes:
    # Load the corpus


    print("Encoding corpus sentences...")
    corpus_embeddings = [model.encode(sentence) for sentence in tqdm(corpus_sentences, desc="Encoding Sentences")]

    pc.create_index(name=index_name, metric="cosine", dimension=corpus_embeddings[0].shape[0])

    # Initialize the index
    index = pc.Index(index_name=index_name)

    # Add the corpus embeddings to the Pinecone index
    item_ids = [str(i) for i in range(len(corpus_embeddings))]
    corpus_embeddings_list = [embedding.tolist() for embedding in corpus_embeddings]
    index.upsert(list(zip(item_ids, corpus_embeddings_list)))
else:
    # Initialize the existing index
    index = pc.Index(index_name=index_name)

# Load Falcon 7B Instruct Model
falcon_model_name = 'tiiuae/falcon-7b-instruct'
falcon_tokenizer = AutoTokenizer.from_pretrained(falcon_model_name, trust_remote_code=True)
falcon_model = AutoModelForCausalLM.from_pretrained(falcon_model_name, trust_remote_code=True)

# Chatbot Function
def chatbot():
    while True:
        query = input("You: ")
        query_embedding = model.encode([query], show_progress_bar=True).tolist()[0] # Get the first element
        res = index.query(vector=query_embedding, top_k=1, include_values=True)
        if res.matches:
            closest_text = corpus_sentences[int(res.matches[0].id)]
            inputs = falcon_tokenizer.encode(closest_text, return_tensors="pt")
            outputs = falcon_model.generate(inputs, max_length=100)
            response = falcon_tokenizer.decode(outputs[0], skip_special_tokens=True)
            print("Bot:", response)
        else:
            print("Bot: Sorry, I couldn't find an answer to that question.")

chatbot()