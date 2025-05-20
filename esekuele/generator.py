import re
from .schema import extract_table_names


def generate_sql(engine: str, schema: str, prompt: str) -> str:
    """Return a simple SQL query for the given prompt.

    This minimal implementation only recognizes prompts asking to list all
    rows from a table that appears in the provided schema. If no table is
    recognized, a dummy query is returned.
    """
    tables = extract_table_names(schema)
    for table in tables:
        pattern = rf"(list|show).*{table}"
        if re.search(pattern, prompt, re.IGNORECASE):
            return f"SELECT * FROM {table};"

    return "SELECT 1;"

