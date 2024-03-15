import sys
import os
from vertexai.language_models import CodeGenerationModel
from google.oauth2 import service_account
import vertexai
import re
import json
import requests

# credentials = service_account.Credentials.from_service_account_file("vertex-ai-service-account.json")
credentials_data={
  "type": "service_account",
  "project_id": "symbolic-bit-398912",
  "private_key_id": "6cc13a1aa736855f25148aa6daa2f99374307180",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClM+Eub91x2IhM\nMw5sID2+JwvHI9cRtE5BpIq13BXlN87z8gnKDUIfRQslGpg2pIk+IvizweKy8lmq\nOrA7XPLVFQl3JEvzq9xKbMAaLoOUS6rOf9ik157TPDw+m3JnL4VwNrjhplqWbU+X\nmCXc1hxdX2cm5SM2VZUE5vgco32/IKKvv511E6JUQSeFzB95/4XKkPO2xADcmams\n+6ngxJMRkuF6u1DZyWFkpCzYB/gCaX+HnHEiPm3doYOdb+i3fXuVBZ5y0V2zEcpz\nZeDpbZO7hmWQxPOnjCLWHbqIeCJreDbDdHMelkyv67g1Q9NRwTCLb8RfmeGzMvTo\nv9KJkr0pAgMBAAECggEAARo3hnfN99SEvv1tkIsmiP5PCyUnakF/GYZfkUHGuPYx\nC1pcy7G1nz/MCJNaMK3TEfcUcclOxKLutj7DWPdl0huHKfm0CAw9jBbtsT8I4b8f\nhKvrENk01h6wyDor/pmdP60dzrkCzGjY/x9PdrR3EVMcUnDKVgfRgWwz0P0bpGAw\nnrl6OkOMlQX2Psk0ekWI/WS5Tvt4G3P5VJNeoOdtRQEKvR+qaR3CIJyGafX0RrE8\n0PT2bYUeRP3A2+p1Si7Y6j3E/Kor+mwOjzro2Yl5eANwZMc3sYRxB3hKKAv5StNB\njU804hfJkfMGn46yy1altAUG9s9bq4P+qllgko7+AQKBgQDhrtm/JUAoUh7ew3c6\n89L5rtqZIdZkDoyTFEqQEhu1pN+RILL5J5TLtACmCzBFnW0VNfh0B5bDCuRlstoU\nNK5bdeeQmmeZmP617XB4rakKw0yrOMdu77+RMaGPegVr/bs5xgQjPg5iOrxIEL0r\nduaWYVp5wjW+YksFzmGEu1NIlQKBgQC7ZSIwahplYWzb1WKXj+wy+rWNfEce/yyh\nM5lfHEknUZdd6cu8s6rhkjVEkIeO5OFiylr7pqDEH/5gD6r6YSr4db25sFH5m51u\nsl3yHk9Dam0AdeBdQ21rc1Khfl8ycuFzSwsgSYEWtZ3uoWkud6spxiS3Mqp9uz+i\nBgz75Fs5RQKBgBvSITemEO2nifSuJfGXgyeSfZIpELPO81diRfrSsKXIyGKspEOA\ntKAT9YyCjpXWXU8jExjCorwyiItc6/NXtzLBKyWxUxolOSkWNyo5RkB0aOwmmLc9\nSOFOO/ti8G4qnjz2AyaRDNbhJLrBjYBhLPXW1H90CIoKtfLmSTFConatAoGBAIfH\nDk+gAUIlphdedBI28MA7UWKTgoCeCTs/xMfaGdMIVjFwnfM7Bvxr0Ha+dcn+YqQO\n1H9zyxZvzALUN2E1GEpwHSi27Z56t0YmrNUqSuog6ZukzQ0mNtjc9SkYBGfsPxgn\nbodVWtgWfbkScMB/aqBY9e9bIZb6HnAKDExSuBo1AoGAJnAsYFHyeDs8ZFaVGhPO\nGeYXTMj9JGwZHR+wqFfuiBIqs/cra3xETIDyr6cGT9xTjQ0nVazvROBANgkU+YIO\nWxzzc77PnpfP20yMMTNsJFoZhSQUns8LY9hxzKSnPYURqf32HTTImmmCbz2RJAyO\nOvPWkmJDkDvalolS6HNnEPE=\n-----END PRIVATE KEY-----\n",
  "client_email": "vertex-ai-service-account@symbolic-bit-398912.iam.gserviceaccount.com",
  "client_id": "114836232517254252283",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vertex-ai-service-account%40symbolic-bit-398912.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
credentials = service_account.Credentials.from_service_account_info(credentials_data)



vertexai.init(
    project="symbolic-bit-398912",
    location="us-central1",
    credentials=credentials
)


# API_KEY ="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"
API_KEY ="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"





CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    'Content-Type': 'application/json'
}



def extract_function_names(code):
    # Regular expression to match function names
    function_name_regex = r'(?<!\.)\b(\w+)\s*\([^)]*\)(?:\s*:\s*\w+)?\s*{'

    # Find all function names in the code
    function_names = re.findall(function_name_regex, code)
    

    # List of keywords associated with conditional blocks, loops, and nested functions
    keywords_to_exclude = ['if', 'else', 'for', 'while', 'else if', 'switch', 'function', 'ngOnChanges', 'ngOnInit', 'ngDoCheck', 'ngAfterContentInit', 'ngAfterContentChecked', 'ngAfterViewInit', 'ngAfterViewChecked', 'ngOnDestroy','constructor']


    # Filter out unwanted function names
    filtered_names = [name for name in function_names if name not in keywords_to_exclude]

    return filtered_names





def extract_function_code(code, method_name):
    method_code = []
    in_method = False
    opening_braces = 0
    closing_braces = 0

    # Start and end markers for the method
    start_marker = f"{method_name}("
    end_marker = "}"

    # Iterate through each line of the code
    for line in code.split('\n'):
        # Check if the line contains the start of the current method
        if start_marker in line:
            in_method = True
            method_code.append(line.strip())
            opening_braces += line.count('{')
            closing_braces += line.count('}')

        # Check if we're inside the current method
        elif in_method:
            # Add the line to the method code
            method_code.append(line.strip())
            opening_braces += line.count('{')
            closing_braces += line.count('}')

            # Check if we've reached the end of the method
            if opening_braces > 0 and opening_braces == closing_braces:
                in_method = False

    # Join the lines of the method code
    method_code = '\n'.join(method_code)

    return method_code


# def send_api_request(code):
#     try:
#         prompt = "Generate unit test cases using jasmine frameworks for below angular code . Try to generate proper unit test casces per defined functions."
#         parameters = {
#             "max_output_tokens": 8192,
#             "temperature": 0.6
#         }
#         model = CodeGenerationModel.from_pretrained("code-bison-32k")
#         response = model.predict(
#             prefix=prompt + code,
#             **parameters
#         )
#         return response.text

#     except Exception as e:
#         # Handle exceptions and return None
#         print(f"Exception: {e}")
#         return None
    
# For getting the code of function

def explain_api_request(code):
   
    prompt =f"You are angularjs unit testing expert. Your job is to first understand the given code {code} then explain the code so that every team member should understand the logic and working of the function"
    
#     try:
#         prompt1 = prompt
#         parameters = {
#     "max_output_tokens": 8000,
#     "temperature": 0.2
# }
#         model = CodeGenerationModel.from_pretrained("code-bison-32k")
#         response = model.predict(
#             prefix=prompt1,
#             **parameters
#         )
#         return response.text

#     except Exception as e:
#         # Handle exceptions and return None
#         print(f"Exception: {e}")
#         return None
    
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(CHAT_API_URL, json=payload, headers=HEADERS, auth=('', API_KEY))
    if response.status_code != 200:
        raise Exception(response.text)
    
    choices = response.json().get('choices', [])

    if len(choices) == 0:
        raise Exception("Prompt did not return any answer")   
    message = choices[0].get("message", {}).get("content", "")
    # print(message, "message")
    return message

def open_api_request(code, type, number, context):
   
    prompt = f"You are angularjs unit testing expert. Your job is to write {number} numbers of {type} type sceanrios for the given code {code} using the explaination of its working here {context}. Your job is to achieve maximum code coverage.Generate scenarios from the given {context} only. It is mandatory that each  numbers of {type} type scenarios genereated by you  should be different from each other , means not alike / same type. Try to cover all the possible different corner cases in these scenarios."
    

#     try:
#         prompt1 = prompt
#         parameters = {
#     "max_output_tokens": 8000,
#     "temperature": 0.5
# }
#         model = CodeGenerationModel.from_pretrained("code-bison-32k")
#         response = model.predict(
#             prefix=prompt1,
#             **parameters
#         )
#         return response.text

#     except Exception as e:
#         # Handle exceptions and return None
#         print(f"Exception: {e}")
#         return None
    
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8
    }

    response = requests.post(CHAT_API_URL, json=payload, headers=HEADERS, auth=('', API_KEY))
    if response.status_code != 200:
        raise Exception(response.text)
    
    choices = response.json().get('choices', [])

    if len(choices) == 0:
        raise Exception("Prompt did not return any answer")   
    message = choices[0].get("message", {}).get("content", "")
    # print(message, "message")
    return message

def generate_api_request(code, context, type, number):
    prompt = f"You are angularjs unit testing expert. Your job is to write {number} high quality unit test code using jest framework for given angular function: {code} for the given {type} scenarios in the context: {context}. Striclty go through the context and generate unit test code with description including assertions cvoering all scenarios in one file. "
    # print(prompt)
#     try:
#         prompt1 = prompt
#         parameters = {
#     "max_output_tokens": 8000,
#     "temperature": 0.6
# }
#         model = CodeGenerationModel.from_pretrained("code-bison-32k")
#         response = model.predict(
#             prefix=prompt1,
#             **parameters
#         )
#         return response.text

#     except Exception as e:
#         # Handle exceptions and return None
#         print(f"Exception: {e}")
#         return None
    
    payload = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.8
    }

    response = requests.post(CHAT_API_URL, json=payload, headers=HEADERS, auth=('', API_KEY))
    if response.status_code != 200:
        raise Exception(response.text)
    
    choices = response.json().get('choices', [])

    if len(choices) == 0:
        raise Exception("Prompt did not return any answer")   
    message = choices[0].get("message", {}).get("content", "")
    # print(message, "message")
    return message      

def generate_api_request1(code, response, type, number):
    prompt = f"You are angularjs unit testing expert.Here is the current generated unit test cases:{response}, for input code:{code} . Your task is to improve all these current unit test cases on {type} type scenarios. If the unit test cases you are getting that are not implemented , you have to fully implement it accurately using jest framework.It is mandatory that every unit test cases should be implemented completely."
    # print(prompt)
    try:
        prompt1 = prompt
        parameters = {
    "max_output_tokens": 8000,
    "temperature": 0.6
}
        model = CodeGenerationModel.from_pretrained("code-bison-32k")
        response = model.predict(
            prefix=prompt1,
            **parameters
        )
        return response.text

    except Exception as e:
        # Handle exceptions and return None
        print(f"Exception: {e}")
        return None
    
    # payload = {
    #     "model": "gpt-3.5-turbo-16k",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ],
    #     "temperature": 0.8
    # }

    # response = requests.post(CHAT_API_URL, json=payload, headers=HEADERS, auth=('', API_KEY))
    # if response.status_code != 200:
    #     raise Exception(response.text)
    
    # choices = response.json().get('choices', [])

    # if len(choices) == 0:
    #     raise Exception("Prompt did not return any answer")   
    # message = choices[0].get("message", {}).get("content", "")
    # # print(message, "message")
    # return message   
def send_api_request(code,type, number):
    prompt = f"You are angularjs unit testing expert. Your job is to first understand the given code {code} and then write unique {number} {type} scenarios not the test code only the behaviours. Your job is to achieve maximum code coverage. Do not hallucinate and generate scenarios from the given code only "

    try:
        prompt1 = prompt
        parameters = {
    "max_output_tokens": 8000,
    "temperature": 0.2
}
        model = CodeGenerationModel.from_pretrained("code-bison-32k")
        response = model.predict(
            prefix=prompt1,
            **parameters
        )
        return response.text

    except Exception as e:
        # Handle exceptions and return None
        print(f"Exception: {e}")
        return None
    
# for getting the happy path & negative cases scenarios
def send_api_request1(code,context,type, number):
    prompt = f"You are angularjs unit testing expert. Your job is to write high quality unit tests using jest framework for given angular code {code} for the given {type} scenarios in the context {context}. Please ensure you write test case and test desription for each {number} scenarios given in the context.Write the common part used in each test case at the top only "

    try:
        prompt2 = prompt
        parameters = {
            "max_output_tokens": 8192,
            "temperature": 0.2
        }
        model = CodeGenerationModel.from_pretrained("code-bison-32k")
        response = model.predict(
            prefix=prompt2,
            **parameters
        )
        return response.text

    except Exception as e:
        # Handle exceptions and return None
        print(f"Exception: {e}")
        return None
    
    

# for gettting code of happy path & negative cases scenarios
def generate_tests(file_name):
    try:
        with open(file_name, 'r') as file:
            file_content = file.read()
            function_names = extract_function_names(file_content)
            # print("Function Names:", function_names)

            # Prompt user for private key
            private_key = input("Enter your private key: ")

            # Check if the provided private key matches the expected key
            if private_key == "gc_spgrXSnfZqYSVqqhQiVjlYApSQofFXIUtF":
                print("Function Names:", function_names)
                # Extract function code for each function name
                for function_name in function_names:
                    function_code = extract_function_code(file_content, function_name)
                    # print("\nFunction:", function_name)
                    # print("Code:\n", function_code)

                    behaviour_type = [{"type": "HappyPath", "number": 6}, {"type": "EdgeCase", "number": 6}, {"type": "NegativeCase", "number": 6}]

                    explain_response = explain_api_request(function_code)

                    for obj in behaviour_type:
                        
                        type = obj['type']
                        print(f"Generating tests for '{type}' scenarios for '{function_name}' function")
                        api_response = open_api_request(function_code, obj['type'], obj['number'], explain_response)
                        # print(api_response)
                        test_response = generate_api_request(function_code, api_response, obj['type'], obj['number'])
                        test_response1 = generate_api_request1(function_code, test_response,obj['type'], obj['number'])
     
                       
                        if test_response:
                            directory_path = os.path.dirname(file_name)
                            test_folder_path = os.path.join(directory_path, 'gocodeo_tests')
                            os.makedirs(test_folder_path,exist_ok=True)
                            function_test_folder_path = os.path.join(test_folder_path, function_name)
                            os.makedirs(function_test_folder_path,exist_ok=True)
                            # Write API response (test cases) to a test.py file in the same directory
                            output_file_path = os.path.join(function_test_folder_path, f'test_{function_name}_{type}.ts')
                            
                            if (test_response1.startswith("```typescript") or test_response1.startswith("```javascript")) and test_response1.endswith("```"):
    
                                start_markers = ["```typescript", "```javascript"]
                                end_marker = "```"
                                start_index = -1
                                end_index = -1


                                end_index = test_response1.rfind(end_marker)

                                for marker in start_markers:
                                    start_index = test_response1.find(marker)
                                    if start_index != -1:
                                        break
    
                                if start_index != -1 and end_index != -1:
                                    # Extract content between start and end markers
                                    start_marker_length = len(start_markers[start_index])
                                    content = test_response1[start_index + start_marker_length:end_index].strip()
                                else:
                                    content = test_response1
                            else:
                                content = test_response1

                        

                            with open(output_file_path, 'w') as output_file:
                                output_file.write(content)
                                print(f"Test cases for '{function_name}' written to {output_file_path}")
                        else:
                            print(f"Failed to fetch test cases from API for function '{function_name}'.")        
                        
                    # Send API request with fetched code
                    # if function_name != 'if' or function_name != 'for':
                    #     api_response = open_api_request(function_code)
                    #     print('edge cases below')
                    #     print(api_response)
                        # api_response1 = send_api_request1(function_code,api_response)
                        # print('code of edge cases')
                        # print(api_response1)

                        # if api_response1:
                        #     directory_path = os.path.dirname(file_name)
                        #     test_folder_path = os.path.join(directory_path, 'gocodeo_tests')
                        #     os.makedirs(test_folder_path,exist_ok=True)
                        #     # Write API response (test cases) to a test.py file in the same directory
                        #     output_file_path = os.path.join(test_folder_path, f'test_{function_name}.ts')
                        #     with open(output_file_path, 'w') as output_file:
                        #         output_file.write(api_response1)
                        #         print(f"Test cases for '{function_name}' written to {output_file_path}")
                        # else:
                        #     print(f"Failed to fetch test cases from API for function '{function_name}'.")
            else:
                print("Invalid private key. Access denied.")

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")

def generate_tests_cli():
    if len(sys.argv) != 3:
        print("Usage: gocodeo generate <file_name>")
        sys.exit(1)
    
    file_name = sys.argv[2]
    generate_tests(file_name)

if __name__ == "__main__":
    generate_tests_cli()