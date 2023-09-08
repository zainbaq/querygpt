# Welcome to QueryGPT!

Here we are trying to build a system that can process human language and retrieve data from your databases based on your request.

The application works by connecting to your database, and reading the schema of all tables in that database. That schema is processed and fed into OpenAIs ChatGPT as a context so that users can ask it questions about the database.

So far the support DB types are:
- SQLite3
- MySQL

Upcoming DB support:
- MS SQL
- Redshift

## Quickstart

### Set up your OpenAI API key
Create a file called `.env` and in that file add the following line.
```
OPENAI_KEY=<your-openai-api-key-here>
```

### Build the virtual environment and run the bot
```
bash build.sh
source querygpt/bin/activate # if not already activated
python app/bot.py -e <engine> -f <path/to/config/file> -m <openai model>
```
The config files contain relevant information on the database you want to connect to.

## SQLite3
For SQLite3, this simply points to the .db file.

## MySQL
For MySQL, create a JSON file in `database/mysql/<table_name>.json` and have it contain the following lines.
```
{
  "host": endpoint to your DB instance,
  "database": database name,
  "user": login username,
  "password": login password
}
```