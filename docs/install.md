# Install

## Run locally
- Create a file named '.env' within the project directory with the following contents:
- Replace the contents of DISCORD_BOT_TOKEN with the tokens obtained during the creation of the Discord.
- Here, the DB is using MySQL.

```
DB_HOST = "example_host"
DB_PORT = "3306"
DB_USER = "example_user"
DB_PASSWORD = "example_password"
DB_SCHEMA = "example_schema"
DB_TABLE = "example_table"
DISCORD_BOT_TOKEN = "{replace_me}"
```
## Use Host Run

```
poetry install
```

```
poetry run python3 main.py
```