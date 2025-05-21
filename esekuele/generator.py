import re
from .schema import extract_table_names


def generate_sql(engine: str, schema: str, prompt: str) -> str:
    """Return a simple SQL query for the given prompt.

    The implementation recognizes prompts asking to list all rows or count
    rows from a table that appears in the provided schema. If no table is
    recognized, a dummy query is returned.
    """
    tables = extract_table_names(schema)
    for table in tables:
        list_pattern = rf"(list|show).*{table}"
        if re.search(list_pattern, prompt, re.IGNORECASE):
            return f"SELECT * FROM {table};"

        count_pattern = rf"(count|how many).*{table}"
        if re.search(count_pattern, prompt, re.IGNORECASE):
            return f"SELECT COUNT(*) FROM {table};"

    return "SELECT 1;"

