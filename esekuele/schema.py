import re


def extract_table_names(schema: str) -> list[str]:
    """Return a list of table names found in a simple schema string."""
    names = re.findall(r"(\w+)\s*\(", schema)
    return names

