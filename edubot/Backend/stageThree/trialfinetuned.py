from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModelForCausalLM, PeftConfig

def load_model():
    model_id = "kings-crown/EM624_QA_Multi"
    base_model_id = "meta-llama/Llama-2-13b-chat-hf"
    access_token = "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"
    base_model = AutoModelForCausalLM.from_pretrained(base_model_id, use_auth_token=access_token)
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_auth_token=access_token)
    config = PeftConfig.from_pretrained(model_id, use_auth_token=access_token)
    model = PeftModelForCausalLM(base_model, config)

    return model, tokenizer

def generate_response(model, tokenizer, query):
    inputs = tokenizer.encode(query, return_tensors='pt')
    output = model.generate(inputs, max_length=512, num_return_sequences=1, temperature=1.0)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return response_text

def main():
    model, tokenizer = load_model()
    print("Model loaded. You can start chatting. Type 'quit' to exit.")
    while True:
        query = input("You: ")
        if query.lower() == 'quit':
            break
        response = generate_response(model, tokenizer, query)
        print("Bot:", response)

if __name__ == "__main__":
    main()
