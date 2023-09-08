import openai
from utils import get_openai_key
from connectors.sqlite import SQLiteDBConnector
from connectors.mysql import MySQLConnector
import json
import argparse

openai.api_key = get_openai_key()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', default='gpt-3.5-turbo', type=str)
    parser.add_argument('--engine', '-e', type=str, default='sqlite3')
    parser.add_argument('--file', '-f', required=True, type=str)
    return parser.parse_args()

def get_connector_from_engine(engine, **kwargs):
    if engine == 'sqlite3':
        db_parser = SQLiteDBConnector(kwargs.get('file'))
    elif engine == 'mysql':
        db_parser = MySQLConnector(kwargs.get('file'))
    else:
        print('Provided engine is not implemented yet. Supported engines are: sqlite3')
        raise NotImplementedError
    return db_parser

def converse(args, schema_string, connector=None):
    while True:

        question = input('>> ')
        if question == 'exit' or question == 'quit':
            break

        prompt = f"Answer the question based on the database schema below, and if the question can't be answered based on the context, say \"I don't know\"\n\nProvide only the answer and no other conversational fluff.Context: {schema_string}\n\n---\n\nQuestion: {question}\nAnswer:"

        system_message = {"role": "system", "content": f"You are an expert in {args.engine} querying and are assisting a Data Engineer"}
        messages = [system_message]
        messages.append({"role":"user","content":prompt})

        response = openai.ChatCompletion.create(
            messages=messages,
            model=args.model
        )
        # messages.append(response['choices'][0]['message'])
        answer = response['choices'][0]['message']['content']
        print(answer)
        print(connector.execute_query(answer))

def main():
    args = parse_args()

    # Get parser for DB engine and then get the schemas of each table in the DB
    db_connector = get_connector_from_engine(args.engine, file=args.file)
    schemas = db_connector.get_schemas()

    # Convert schemas dict into a string parseable by ChatGPT
    schema_string = json.dumps(schemas, indent=2)
    
    converse(args, schema_string, connector=db_connector)

if __name__ == '__main__':
    # 
    args = parse_args()
    main()
    
