from __future__ import annotations

import re
from typing import Dict

from .schema import extract_table_names


class Provider:
    """Base class for SQL generation providers."""

    def generate(self, engine: str, schema: str, prompt: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class RegexProvider(Provider):
    """Simple regex-based implementation used as a fallback."""

    def generate(self, engine: str, schema: str, prompt: str) -> str:
        tables = extract_table_names(schema)
        for table in tables:
            list_pattern = rf"(list|show).*{table}"
            if re.search(list_pattern, prompt, re.IGNORECASE):
                return f"SELECT * FROM {table};"

            count_pattern = rf"(count|how many).*{table}"
            if re.search(count_pattern, prompt, re.IGNORECASE):
                return f"SELECT COUNT(*) FROM {table};"

        return "SELECT 1;"


class OpenAIProvider(Provider):
    """Provider that delegates query generation to the OpenAI API."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

    def generate(self, engine: str, schema: str, prompt: str) -> str:
        import openai  # imported here to allow testing without the package installed

        system_prompt = (
            "You are a SQL assistant. "
            f"Use the {engine} dialect. The database schema is: {schema}."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response["choices"][0]["message"]["content"].strip()


PROVIDERS: Dict[str, Provider] = {
    "regex": RegexProvider(),
    "openai": OpenAIProvider(),
}


def register_provider(name: str, provider: Provider) -> None:
    """Add a provider to the registry."""
    PROVIDERS[name] = provider


def get_provider(name: str) -> Provider:
    return PROVIDERS[name]


def generate_sql(
    engine: str, schema: str, prompt: str, provider: str = "regex"
) -> str:
    """Return a SQL query for the given prompt using the selected provider."""
    provider_obj = get_provider(provider)
    return provider_obj.generate(engine, schema, prompt)
