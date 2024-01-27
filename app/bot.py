import openai
from utils import get_openai_key
from connectors.sqlite import SQLiteDBConnector
from connectors.mysql import MySQLConnector
import json
import argparse
import pandas as pd

openai.api_key = get_openai_key()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='gpt-3.5-turbo', type=str)
    parser.add_argument('--engine', '-e', type=str, default='sqlite3')
    parser.add_argument('--file', '-f', required=True, type=str)
    return parser.parse_args()

# Engine selector
def get_connector_from_engine(engine, **kwargs):
    if engine == 'sqlite3':
        db_parser = SQLiteDBConnector(kwargs.get('file'))
    elif engine == 'mysql':
        db_parser = MySQLConnector(kwargs.get('file'))
    else:
        print('Provided engine is not implemented yet. Supported engines are: sqlite3')
        raise NotImplementedError
    return db_parser

# This method provides a sliding window approach so as not to provide too many tokens to the LLM
def get_inputs_from_conversation(messages, buffer=2) -> list:
    if buffer > len(messages):
        return [messages[-1]]
    else: return messages[-buffer:]

# Determine whether or not to prompt user to run the query
# This can be done using an LLM too, but for now, it is using simple string matching for this criteria
def contains_action_keyword(input_string: str) -> bool:
    common_keywords = ["write", "get", "search", "retrieve", "execute", "perform", "do", "run"]

    # Convert the input string to lowercase for case-insensitive matching
    lowercased_input = input_string.lower()

    # Check if any common keyword is present in the input string
    for keyword in common_keywords:
        if keyword in lowercased_input:
            return True
    return False

# Function to initiate a conversation with the LLM. Conversations are retained by storing each message
# in a list and exposing the last `buffer` messages to the LLM (for token efficiency)
#
# Also includes an option to run the query in the database to retrieve the data
def converse(args, schema_string: str, connector=None, buffer: int=2):

    # Provide instructions to the LLM as a system message
    system_message = {"role": "system", "content": f"You are an expert in {args.engine} querying and are assisting a Data Engineer"}
    
    # Create a list to store the conversation history and add the system message to it
    messages = [system_message] 

    # Start conversation loop
    while True:
        
        # Get prompt as an input from the user
        question = input('>> ')

        # Break conversation when 'exit' or 'quit' is input by the user
        if question.lower() == 'exit' or question.lower() == 'quit':
            break
        
        # Prompt engineering
        prompt = f"Answer the question based on the database schema below. Provide only the answer and no other conversational fluff.\n\nSchema: {schema_string}\n\n---\n\nQuestion: {question}\nAnswer:"
        messages.append({"role" : "user", "content" : prompt}) # Add user prompt to conversation

        # Get LLM inputs from conversation based on buffer length
        inputs = get_inputs_from_conversation(messages, buffer=buffer)

        # Call LLM for response for given inputs
        response = openai.ChatCompletion.create(
            messages=inputs,
            model=args.model
        )
            
        answer = response['choices'][0]['message']['content']
        messages.append({"role" : "assistant", "content" : answer})
        print(f"\nResponse: \n{answer}")

        # Prompt user for permission to run query
        if contains_action_keyword(question):
            run_query = input("Run this query? (yes|no) >> ")
            if run_query.lower() == 'yes':
                try:
                    output = connector.execute_query(answer)
                    print(pd.DataFrame(output))
                except Exception as e:
                    print("It seems like there is an issue with this query. Please verify the query.")
                    print(e)

def main():
    args = parse_args()

    # Get parser for DB engine and then get the schemas of each table in the DB
    db_connector = get_connector_from_engine(args.engine, file=args.file)
    schemas = db_connector.get_schemas()

    # Convert schemas dict into a string parseable by ChatGPT
    schema_string = json.dumps(schemas, indent=2)
    
    # Run conversation
    converse(args, schema_string, connector=db_connector)

if __name__ == '__main__':
    args = parse_args()
    main()