from stageOne.QnAmodel import get_answer
from stageThree.responseModel import response_generator

def main():
    while True:
        user_input = input("You: ")

        # Passing the input to the stage 1 component
        data = get_answer(user_input)

        # If the response was 0, it means we need to go to the stage 2 component
        if data == '':
            # data = KUNAL_MODEL  # Implement your model function here
            pass  # Placeholder for stage 2 component

        # Now we pass the data to the stage 3 component. For now I have used the same model professor had used in his code,
        # But I belive we should use Llama or something with more dialogue generative ability. Please feel free to try using LLama 
        response = response_generator(data)

        print("Chatbot:", response)

if __name__ == "__main__":
    main()
