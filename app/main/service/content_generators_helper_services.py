# import openai
import os
import requests
import json

from dotenv import load_dotenv
import openai
import os


load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")

# fireworks_model = "accounts/fireworks/models/mixtral-8x7b-instruct"


def title_gen(note):
    """Generate a title for a conversation based on a given note.

    Args:
        note (str): The note to base the title on.

    Returns:
        str: The generated title.
    """
    try:
        messages = [
            {
                "role": "system",
                "content": f"""
                    You are an Data Analyst Assistant.
                    
                    You are an expert analyst assitant, given this start up conversation: "{note}". 
                    you are to generate a not more than five words title name for this conversation.
                    the title name should be comprehensive, educative and contextual 
                    of not more than five words. don't add any description or text apart from 
                    the name, generate only the title name.
                    
                    
                    """,
            }
        ]

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
            messages=messages,
        )
        
        name =  response["choices"][0]["message"]["content"]
        return name
    except Exception as e:
        print(f"title_gen Format Error: {e}")


def answer_step(query, context):
    """Generate a response to a user query based on a given context.

    Args:
        query (str): The user's query.
        context (str): The contextual information used to generate the response.

    Returns:
        str: The generated response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""you expert data analysts, your task is to assist the user. from this given context: {context}. you job is to answer 
                                            answering the query directly. below is the user question""",
            },
            {"role": "user", "content": query},
        ],
    )

    return response["choices"][0]["message"]["content"]


def reasoning_phase(summary, query, metadata):
    """Generate reasoning steps to a user query based on a given context.

    Args:
        summary (str): The summary of the previous conversation.
        query (str): The user's query.
        metadata (str): The metadata of the uploaded CSV file.

    Returns:
        list: A list of tasks results. Each element is a dictionary containing the action to take and the generated response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""you expert data analysts, you will provide assistant to the user, the assistant will include answering normal english question from the context of previouse conversations and or generating python code for querying pandas dataframe table data that is created from the csv file uploaded by the user to retrieve information if required to answer the user's question completely.
                        here is the summary of your previous conversations with the user: {summary}. the csv file if uploaded has the following columns: {metadata}. 
                       you are provided with 2 tools, 1: text_answer, 2: python_code_execution. given user prompt, you are to reason through and break down the appropraite 
                       response in to chain of steps in the following format, an array of objects, each object is like a step containing the action to take at that step, 
                       example {{"text_answer": "generate text response fir this step"}} or {{"python_execution": "generate the python code to run to retrieve the data, always use print() statement to print the retrieved data, generate accurate and clean 
                    python code from a user query to run on the dataframe. the dataframe is already giving to as 
                    'df', so don't create one. note that the values \n of the dataframe are always lower case. make sure it is only the python code, no any text or description apart from the code"}}.
                        your response must be in this format: [{{"text_answer": "generate text response fir this step"}}, 
                        {{"python_execution": "generate the python code to run to retrieve the data, make sure it is only the python code, no any text or description apart from the code or some indidcation, just the code."}} ]
                        and so on, untill the steps to the user prompt is complete.
                        if the user does not provide any csv file, don't mention the python_code_execution in the steps, instead, encourage the user to upload the data file to get the assistant.
                        generate just the list, only provide a RFC8259 compliant JSON response.
                       """,
            },
            {"role": "user", "content": "here is the user prompt or query :" + query},
        ],
        temperature=0.3,
        max_tokens=1473,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return json.loads(response["choices"][0]["message"]["content"])



def final_response_gen(prompt, tasks_results):
    """Generate the final response to the user query.

    Args:
        prompt (str): The user prompt.
        tasks_results (list): The list of tasks results. Each element is a dictionary containing the action taken and the generated response.

    Returns:
        str: The final response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""you are expert data analysts, your task is to assist the user. you are to generate appropriate comprehensive summary higlighting the key points from these given contextual steps to answer the user prompt, here is the user prompt. below is the user prompt and the contextual steps""",
            },
            {"role": "user", "content": f"here is the user prompt :{prompt}. \n and here are the contextual steps followed for answering the question: {tasks_results}" },
        ],
    )

    return response["choices"][0]["message"]["content"]


