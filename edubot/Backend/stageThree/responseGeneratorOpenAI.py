import openai

openai.api_key = "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"

def response_generator(question, context):
    openai.api_key = "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"

    # Combine question and context into one input string
    input_text = f"Question: {question}\nContext: {context}"

    # # Use the GPT-3.5 API to generate a response
    # response = openai.Completion.create(
    #     engine="text-davinci-003",  # You can choose other engines as well
    #     prompt=input_text,
    #     max_tokens=150,  # You can adjust the max tokens as needed
    #     n=1,
    #     stop=None,
    #     temperature=1.0
    # )

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "you are Professor who loves his students and is very empathetic, wise and knowledgeable. You will respond only with information given in the context, if the context is empty, you will say that you do not know the answer to that yet. Do not hallucinate and give extra information."
        },
        {
          "role": "user",
          "content": input_text
        },
      ],
      temperature=1,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n"]
    )


    # Extract and return the generated text from the API response
    response_text = response['choices'][0]['message']['content'].strip()

    return response_text

# Example usage:
#question = "Who is Naveen?"
#context = "Naveen is a graduate student at stevens institute of technology who is very interested in AI. Naveen is from Bahrain, a small island in the Middle East but his homeland is Kerala, India"

#print(response_generator(question, context))
