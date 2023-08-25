# importing the required libraries
from transformers import pipeline
from datetime import datetime
from time import time

# providing the input phrase and parameters
input_sentence = 'ask the instructor'
num_sequences_return = 1
out_max_length = 20
token_id = 50256
#selected_model = 'gpt2'
selected_model = 'bigscience/bloom-560m'
#selected_model = 'EleutherAI/gpt-neo-1.3B'
#selected_model = 'EleutherAI/gpt-j-6B'

# printing the starting time
start_time = datetime.now()
print ('\n-Starting the text generation process for the sentence','\n ---', input_sentence,'---\n' 'at {}'.format(start_time), '\n')
t = time()

# creating the text generation using the given model
generator = pipeline('text-generation', model = selected_model, pad_token_id = token_id)

# generating the text
text = generator(input_sentence, max_length = out_max_length,
                 num_return_sequences = num_sequences_return)

# basic cleaning of the generatted text
out_sentence = text[0]['generated_text'].replace('\n', '')

# printing the output
print(out_sentence)
print('\nTime to generate the text: {} mins'.format(round((time() - t) / 60, 4)))
