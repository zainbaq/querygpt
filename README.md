# Welcome to QueryGPT!

Here we are trying to build a system that can process human language and retrieve data from your databases based on your request.

So far the support DB types are:
- SQLite3
- MySQL

Upcoming DB support:
- MS SQL
- Redshift

## Quickstart
```
python app/bot.py -e <engine> -f <path/to/config/file> -m <openai model>
```

The config files contain relevant information on the database you want to connect to.

## SQLite3
For SQLite3, this simply points to the .db file.

## MySQL
For MySQL, create a JSON file in ```database/engine/table_name.json and have it contain the following lines.
```
{
  "host": endpoint to your DB instance,
  "database": database name,
  "user": login username,
  "password": login password
}
```