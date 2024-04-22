import json
import boto3
import io
import os

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    #data = json.dumps(event)
    #print("recieved event: " + str(event))
    query_param = event.get('queryStringParameters', {}).get('query', '')
    print(f"Received query parameter: {query_param}")
    #queryParam = event["queryParam"]
    #query = event.get("query")
    query = query_param
    #payload = data
    payload = {
        "inputs":query,
        "parameters": {
            "max_new_tokens": 1024,
            "do_sample": False,
            "top_p": 0.95,
            "top_k": 40,
            "temperature": 0.5,
            "repetition_penalty": 1.0,
            "stop": ["</|im_end|>"]
          }
    }
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        #Body=bytes(payload, 'utf-8'))
        Body=json.dumps(payload))
    
    result = json.loads(response['Body'].read().decode('utf-8'))
    output = {
        
        #"isBase64Encode": False,
        "statusCode":200,
        #"statusDescription": "200 ok",
        #"headers": {
            "Content-Type": "application/json",
       # },
        "body": json.dumps(result) #str(result[0]["generated_text"])
    }
    return output
    
