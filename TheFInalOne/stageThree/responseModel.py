from transformers import pipeline

def response_generator(data):
    selected_model = 'bigscience/bloom-560m'  # You can change this to the another model, like Llama
    token_id = 50256  #  token ID for the padding token
    out_max_length = 20  # Maximum length of the generated text

    # Creating the text generation pipeline
    generator = pipeline('text-generation', model=selected_model, pad_token_id=token_id)

    # Generating the text based on the input data
    generated_text = generator(data, max_length=out_max_length, num_return_sequences=1)

    # Cleaning the generated text
    response = generated_text[0]['generated_text'].replace('\n', '')

    return response

# Example usage
#input_data = "Barack oBama is a very"
#generated_response = response_generator(input_data)
#print("Generated Response:", generated_response)
