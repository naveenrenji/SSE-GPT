from stageOne.get_answer import get_answer
from stageTwo.SSEmodel import get_SSE_results
from stageThree.responseGenerator import response_generator
from time import time


def get_bot_response(message):
    t=time()
    data = get_answer(message)
    response = data
    # If the response was '', there was no match at stage 1, hence -> stage 2 component
    if data == '':
        response = get_SSE_results(message)  # Implement your model function here
        print(data) # for debugging only
        #pass  # Placeholder for stage 2 component

    # Now we pass the data to the stage 3 component. 
    # But I belive we should use Llama or something with more dialogue generative ability. Please feel free to try using LLama2 
    #response = response_generator(message, data)
    print('Total time:', round(time() - t, 4), 'seconds')
    return response

#print(get_bot_response("what version of python are we using in class?"))

