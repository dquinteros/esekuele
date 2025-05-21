from click.testing import CliRunner
from esekuele.cli import main
from esekuele import __version__
import sys
import types


def test_version_option():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_generate_select_all():
    runner = CliRunner()
    schema = 'users(id int, name text)'
    result = runner.invoke(main, ['--schema', schema, '--engine', 'sqlite', 'list all users'])
    assert result.exit_code == 0
    assert 'SELECT * FROM users;' in result.output


def test_generate_count():
    runner = CliRunner()
    schema = 'orders(id int, amount int)'
    result = runner.invoke(main, ['--schema', schema, 'how many orders'])
    assert result.exit_code == 0
    assert 'SELECT COUNT(*) FROM orders;' in result.output


def test_cli_with_openai(monkeypatch):
    class FakeChat:
        @staticmethod
        def create(model, messages):
            return {"choices": [{"message": {"content": "SELECT 1;"}}]}

    monkeypatch.setitem(sys.modules, 'openai', types.SimpleNamespace(ChatCompletion=FakeChat))
    runner = CliRunner()
    schema = 'users(id int, name text)'
    result = runner.invoke(main, ['--provider', 'openai', '--schema', schema, 'list users'])
    assert result.exit_code == 0
    assert 'SELECT 1;' in result.output

