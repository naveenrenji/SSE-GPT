from stageOne.get_answer import get_answer
from stageTwo.SSEmodel import get_SSE_results
from stageThree.responseModel import generate_response


def get_bot_response(message):
    data = get_answer(message)
    response = data
    # If the response was '', there was no match at stage 1, hence -> stage 2 component
    #if data == '':
        # data = KUNAL_MODEL  # Implement your model function here
        #pass  # Placeholder for stage 2 component

    # Now we pass the data to the stage 3 component. For now I have used the same model professor had used in his code,
    # But I belive we should use Llama or something with more dialogue generative ability. Please feel free to try using LLama 
    #response = generate_response(data)
    
    return response