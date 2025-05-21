from click.testing import CliRunner
from esekuele.cli import main
from esekuele import __version__


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


def test_schema_from_file():
    runner = CliRunner()
    import tempfile
    import os
    with tempfile.NamedTemporaryFile('w', suffix='.sql', delete=False) as tmp:
        tmp.write('items(id int)')
        path = tmp.name
    try:
        result = runner.invoke(
            main,
            ['--schema', path, '--engine', 'sqlite', 'list all items']
        )
        assert result.exit_code == 0
        assert 'SELECT * FROM items;' in result.output
    finally:
        os.remove(path)

