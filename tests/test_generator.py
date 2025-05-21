import types
import sys

import pytest

from esekuele.generator import generate_sql, OpenAIProvider


def make_fake_openai(return_text="SELECT 1;"):
    class FakeChat:
        @staticmethod
        def create(model, messages):
            FakeChat.called_with = {"model": model, "messages": messages}
            return {"choices": [{"message": {"content": return_text}}]}

    return types.SimpleNamespace(ChatCompletion=FakeChat, api_key=None)


def test_openai_provider(monkeypatch):
    fake_openai = make_fake_openai("SELECT 42;")
    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    provider = OpenAIProvider(model="test-model")
    sql = provider.generate("sqlite", "users(id int)", "list users")
    assert sql == "SELECT 42;"
    assert fake_openai.ChatCompletion.called_with["model"] == "test-model"


def test_openai_provider_reads_env(monkeypatch):
    fake_openai = make_fake_openai()
    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    monkeypatch.setenv("OPENAI_API_KEY", "abc123")
    provider = OpenAIProvider()
    provider.generate("sqlite", "users(id int)", "list users")
    assert fake_openai.api_key == "abc123"


def test_generate_sql_with_openai(monkeypatch):
    fake_openai = make_fake_openai("SELECT * FROM users;")
    monkeypatch.setitem(sys.modules, "openai", fake_openai)
    sql = generate_sql(
        "sqlite",
        "users(id int, name text)",
        "list users",
        provider="openai",
    )
    assert sql == "SELECT * FROM users;"

