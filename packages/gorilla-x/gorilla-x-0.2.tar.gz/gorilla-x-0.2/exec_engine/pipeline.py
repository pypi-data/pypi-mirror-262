import requests
import os
from openai import OpenAI
from collections import defaultdict
import exec_engine.execution_engine
from exec_engine.credentials.credentials_utils import *
from exec_engine.execution_engine import SQL_Type, Filesystem_Type, RESTful_Type, POSIX_Type

import re

python_pattern = r"```python\n(.*?)\n```"
sql_pattern = r"```sql\n(.*?)\n```"

PYTHON_EXEC_ENGINE_URL = "http://104.198.255.187:443/gorilla_interpreter"
SQL_EXEC_ENGINE_URL = None

def gorilla_exec(output, lang, mode="Gorilla-Exec-Engine", debug=False, config={}, creds=None):
    try:
        _, code = process_output(output)
    except Exception as e:
        print("An error occured while trying to process output{error}.\nAborted...".format(error=e))
        return
    if mode == "Gorilla-Exec-Engine":
        if lang == 'python':
            response = requests.get(PYTHON_EXEC_ENGINE_URL, json={"code": code}, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            try:
                formatted_response = response.json()
                if not debug:
                    return formatted_response['output']
                else:
                    return formatted_response
            except:
                print("An error occured while trying to execute output on the Gorilla Execution Engine")
                print("Response status: {status}".format(status=response))
                return
        elif lang == 'SQL' or lang == 'sql':
            response = requests.get(SQL_EXEC_ENGINE_URL, json={"code": code, "client_config": config}, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            try:
                formatted_response = response.json()
                return formatted_response
            except Exception as e:
                print("An error occured on Gorilla's execution engine server")
                return

    elif mode == "local":
        try:
            response = exec_engine.execution_engine.python_containerize_and_execute(code, credentials=creds)
            if not debug:
                return response['output']
            else:
                return response
        except Exception as e:
            print("An error occured while trying to execute output locally {e}.\nAborted...".format(e=e))
            return
    else:
        print("Selected mode not found. Aborted...")
        return

def process_output(gorilla_output):
    sections = gorilla_output.split('<<<code>>>:')
    if len(sections) != 2:
        return None, gorilla_output
    info, code = sections
    return info, code

INSTRUCTION_TEXT = """
    You are an assistant that outputs executable Python code that perform what the user requests. 
    It is important that you only return one and only one code block with all the necessary imports inside ```python and nothing else.
    The code block should print the output(s) when appropriate.
    
    This is what the user requests: {request}\n
    """

def execute_prompt(content, credentials = None, api_type=RESTful_Type, openai_model="gpt-4-turbo-preview"):
    client = OpenAI()
    # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
    # if you saved the key under a different environment variable name, you can do something like:
    # client = OpenAI(
    #   api_key=os.environ.get("CUSTOM_ENV_NAME"),
    # )

    if api_type == SQL_Type:
        prompt = content
        pattern = sql_pattern
    elif api_type == RESTful_Type or True:
        prompt = INSTRUCTION_TEXT.format(request=content)

        if credentials:
            #credential comes in a [service_name, value, cred_type] format
            token_in_path = []
            raw_key = []
            try:
                for service_name, value, cred_type in credentials:
                    if cred_type == "path":
                        token_in_path.append([service_name, value])
                    elif cred_type == "raw":
                        raw_key.append([service_name, value])
            except:
                print("Error: credentials have to be passed in as a list of [service_name, value, cred_type] pairs")
                return

            if token_in_path != []:
                cred_paths = {}
                for service_name, value in token_in_path:
                    prefix = "./credentials/" + service_name + "/"
                    cred_paths[service_name] = [prefix + file_name for file_name in os.listdir(value)]

                    prompt += "The credentials (such as API keys) are stored in the following paths: {keys_list}. Open the file(s) to access them".format(keys_list=cred_paths)

            if raw_key != []:
                prompt += "Additionally, these api keys are available for the following services {key_list}".format(
                    key_list=" ,".join("{name}={cred}".format(name=name, cred=cred) for name,cred in raw_key))
            
        else:
            prompt += "Equally importantly, try to do so without requiring any API key. If and only if one is really needed, give the code block assuming those keys are provided."


        pattern = python_pattern

    try:
        response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    except OpenAI.APIError as e:
        if e.status == 429:
            print("Warning: openai gpt4 quota ran out, reverting to gpt3.5.\nUpdate the model setting in your config to keep using this setting")
            response = client.chat.completions.create(
            model="gpt-3.5-turbo-instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    output = response.choices[0].message.content
    #print(output) #Intentionally left here for future debugging purpose
    matches = re.search(pattern, output, re.DOTALL)
    if matches:
        code = matches.group(1)
        return code

def prompt_execute(engine, prompt, services=None, creds=None, max_attempt=3):
    ret = defaultdict(list)
    for _ in range(max_attempt):
        forward_call, backward_call = engine.gen_api_pair(prompt, api_type=RESTful_Type, credentials=creds)
        response = engine.api_executor.execute_api_call(forward_call, services)
        
        if response and response['output']:
            ret['output'].append(response['output'])
            return ret
        elif response and response['debug']:
            ret['debug'].append(response['debug'])
    return ret
