# from transformers import PegasusForConditionalGeneration
# from transformers import PegasusTokenizer
# from transformers import pipeline


# def answer_question(question, context):
#     input_text = f"{context}"
#     # Pick model
#     model_name = "google/pegasus-xsum"

#     # Load pretrained tokenizer
#     pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

#     # Define PEGASUS model
#     pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

#     # Create tokens
#     tokens = pegasus_tokenizer(input_text, truncation=True, padding="longest", return_tensors="pt")
#     # Summarize text
#     encoded_summary = pegasus_model.generate(**tokens)

#     # Define summarization pipeline 
#     # summarizer = pipeline(
#     #     "summarization", 
#     #     model=model_name, 
#     #     tokenizer="google/pegasus-xsum", 
#     #     framework="pt"
#     # )

#     # Create summary 
#     # summary = summarizer(input_text, min_length=30, max_length=150)
#     # response = summary[0]["summary_text"]

#     # Summarize text
#     encoded_summary = pegasus_model.generate(**tokens)

#     # Decode summarized text
#     decoded_summary = pegasus_tokenizer.decode(
#         encoded_summary[0],
#         skip_special_tokens=True
#     )

#     return decoded_summary


# question = "Can you explain the distinction between Users and Programmers in how they perceive computers and their use?"
# context = "Users see computers as a set of tools for tasks like word processing and spreadsheets, while programmers understand the computer's ways and languages. Programmers can also create new tools."

# print(answer_question(question, context))


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def generate_answer(question, context):
    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("potsawee/t5-large-generation-race-QuestionAnswer")
    model = AutoModelForSeq2SeqLM.from_pretrained("potsawee/t5-large-generation-race-QuestionAnswer")
    
    # Prepare the context
    context = context.replace("\n", "")
    
    # Tokenize the context
    inputs = tokenizer(context, return_tensors="pt")
    
    # Generate the output
    outputs = model.generate(**inputs, max_length=100)
    
    # Decode the output
    question_answer = tokenizer.decode(outputs[0], skip_special_tokens=False)
    question_answer = question_answer.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")
    
    # Split the question and answer
    generated_question, generated_answer = question_answer.split(tokenizer.sep_token)
    
    return generated_answer

# Example usage
question = "Can you explain the distinction between Users and Programmers in how they perceive computers and their use?"
context = "Users see computers as a set of tools for tasks like word processing and spreadsheets, while programmers understand the computer's ways and languages. Programmers can also create new tools."


print(generate_answer(question, context))
