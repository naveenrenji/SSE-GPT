from transformers import pipeline
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

dataset = [10, 27, 46, 12.85, 79, 2.67, 33, 50, 89, 5.34]

def perform_operation(operation, dataset):
    operation = operation.lower()
    if 'average' in operation:
        return np.mean(dataset)
    elif 'middle' in operation:
        return np.median(dataset)
    else:
        return None

    
def detect_operation(answer):
    answer = answer.lower()
    if 'average' in answer or 'mean' in answer:
        return 'average'
    elif 'middle' in answer or 'median' in answer:
        return 'middle'
    else:
        return answer


#nlp = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
nlp = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

context = """
Naveen is a graduate research student conducting reasearch on LLMs and experimenting with different models.
Naveen loves mansi.
We have a dataset and we can perform several operations on this dataset. 
We can calculate the mean which is the average or avg value of the dataset. 
We can also calculate the median which is the middle value of the dataset. 
The richest man in the world is Elon Musk and he is the CEO of Tesla. He is also the CEO of Twitter. 
Room theory introduces a novel method to consider subjectivity and general context dependency in text analysis.
Room theory takes into account subjectivity using a computational version of the Framework Theory by Marvin Minsky (1974) leveraging on text vectorization - such as Word2Vec. 
Dr Carlo is a Professor working at Stevens Institute of technology (SIT) and he is conducting research on a Domain Specific Chatbot. 
He has a diverse team of students from different departments working towards the research.
"""

questions = ["Who is the richest man in the world?", "What companies does Elon Musk lead?", "How does room theory take subjectivity into account?", "What is the average of the dataset?", "What is the middle value of the dataset?"]
results = []

# Process the predefined questions
for question in questions:
    answer = nlp(question=question, context=context)['answer']
    operation = detect_operation(answer)
    result = perform_operation(operation, dataset)
    if result is None:
        results.append(f"{answer}")
    else:
        results.append(f"{answer} - {result}")

# Create a pandas DataFrame for visualisation
df = pd.DataFrame(list(zip(questions, results)), columns=["Question", "Answer"])
print(df)

# Interactive chat session
while True:
    user_query = input("\nPlease enter your question: ")
    
    if user_query.lower() == 'end':
        print("Ending the session.")
        break
    
    answer = nlp(question=user_query, context=context)['answer']
    operation = detect_operation(answer)
    result = perform_operation(operation, dataset)
    if result is None:
        print(f"Answer: {answer}")
    else:
        print(f"Answer: {answer} - {result}")
