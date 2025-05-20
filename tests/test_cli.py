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

