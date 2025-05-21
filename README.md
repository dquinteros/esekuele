# Esekuele

Esekuele is a command line tool designed to generate SQL queries from natural language prompts. The CLI accepts a database engine name, a SQL schema describing the tables and columns, and a prompt that states a question to be answered.

Given this information, the application will produce a SQL query suitable for the specified engine that should resolve the question described in the prompt.

## Project Goals
- Provide a simple command line interface.
- Accept engine name and schema as inputs.
- Translate a natural language question into a SQL query.

Development is currently in a planning phase. Implementation details and usage instructions will be added as the project evolves.

## Architecture
Esekuele will be implemented in Python 3. The command line interface will use the `click` package to parse options and arguments. Users provide an engine name, a SQL schema, and a prompt describing the desired outcome. The application forwards this information to a language model service which returns a query tailored for the specified engine.

The planned code layout is:

- `esekuele/cli.py` – CLI entry point and argument parsing
- `esekuele/schema.py` – helpers for schema loading and validation
- `esekuele/generator.py` – logic for calling the language model and formatting the resulting SQL

Additional modules and tests will be added as the project evolves.

## Installation
Create a virtual environment and install dependencies from ``requirements.txt``:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the test suite with ``./pytest -q`` once dependencies are installed.

## Usage Example
Run the CLI with a schema and prompt to generate a query:

```bash
python -m esekuele.cli --schema "users(id int, name text)" "list all users"
```

You can also count rows:

```bash
python -m esekuele.cli --schema "orders(id int, amount int)" "how many orders"
```
