from transformers import BartTokenizer, BartForConditionalGeneration

# Load the fine-tuned BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

def generate_response(text_information, user_query):
    """
    Generates a response using the BART model.

    Args:
      text_information: The text information from stage 1 or stage 2.
      user_query: The user query.

    Returns:
      The generated response text.
    """

    # Combine text information and user query to form the input
    input_text = f"The information I have is: '{text_information}'. Now, to your question: '{user_query}'"

    # Tokenize the input text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # Generate the response using the model
    response = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=1.0)

    # Decode and return the response text
    response_text = tokenizer.decode(response[0], skip_special_tokens=True)

    return response_text

# Example usage:
text_information = "The meaning of life is to be good and do good, that is the key!"
user_query = "What is the meaning of life?"

# Generate the response using the BART model
response = generate_response(text_information, user_query)

# Print the response
print(response)
