import os
import re


def extract_table_names(schema: str) -> list[str]:
    """Return a list of table names found in a simple schema string."""
    names = re.findall(r"(\w+)\s*\(", schema)
    return names


def load_schema(value: str) -> str:
    """Return schema text from VALUE or load it from a .sql file.

    If VALUE points to an existing file with a ``.sql`` extension, the file
    contents are returned. Otherwise ``VALUE`` is returned unchanged.
    """
    if value.endswith(".sql") and os.path.isfile(value):
        with open(value, "r", encoding="utf-8") as f:
            return f.read()
    return value

