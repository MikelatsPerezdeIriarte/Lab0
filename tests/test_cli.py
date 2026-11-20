import pytest
from click.testing import CliRunner
from src.cli import cli


@pytest.fixture
def runner():
    """Fixture that instanciates a CliRunner for all the integration tests"""
    return CliRunner()


def test_cli_remove_missing(runner):
    result = runner.invoke(cli, ["clean", "remove-missing", "1", "", "nan", "2"])
    assert result.exit_code == 0
    assert "['1', '2']" in result.output


def test_cli_fill_missing(runner):
    result = runner.invoke(
        cli, ["clean", "fill-missing", "1", "", "nan", "2", "--fill-value", "0"]
    )
    assert result.exit_code == 0
    assert "['1', 0, 0, '2']" in result.output


def test_cli_fill_missing_default(runner):
    result = runner.invoke(cli, ["clean", "fill-missing", "1", "", "2"])
    assert result.exit_code == 0
    assert "['1', 0, '2']" in result.output


def test_cli_normalize(runner):
    result = runner.invoke(cli, ["numeric", "normalize", "0", "5", "10"])
    assert result.exit_code == 0
    assert "[0.0, 0.5, 1.0]" in result.output


def test_cli_normalize_custom_range(runner):
    result = runner.invoke(
        cli,
        ["numeric", "normalize", "1", "2", "3", "--new-min", "10", "--new-max", "20"],
    )
    assert result.exit_code == 0
    assert "[10.0, 15.0, 20.0]" in result.output


def test_cli_standardize(runner):
    result = runner.invoke(cli, ["numeric", "standardize", "1", "2", "3"])
    assert result.exit_code == 0
    assert "[-1.224744871391589, 0.0, 1.224744871391589]" in result.output


def test_cli_clip(runner):
    result = runner.invoke(
        cli,
        [
            "numeric",
            "clip",
            "1",
            "2",
            "3",
            "4",
            "5",
            "--min-val",
            "2",
            "--max-val",
            "4",
        ],
    )
    assert result.exit_code == 0
    assert "[2.0, 2.0, 3.0, 4.0, 4.0]" in result.output


def test_cli_to_integers(runner):
    result = runner.invoke(cli, ["numeric", "to-integers", "1", "2", "abc", "3.5", "4"])
    assert result.exit_code == 0
    assert "[1, 2, 4]" in result.output


def test_cli_log_transform(runner):
    result = runner.invoke(
        cli, ["numeric", "log-transform", "1", "2.718281828459045", "10"]
    )
    assert result.exit_code == 0
    assert "[0.0, 1.0," in result.output


def test_cli_tokenize(runner):
    result = runner.invoke(cli, ["text", "tokenize", "Hello, World! 123"])
    assert result.exit_code == 0
    assert "['hello', 'world', '123']" in result.output


def test_cli_remove_punctuation(runner):
    result = runner.invoke(cli, ["text", "remove-punctuation", "Hello, World! 123"])
    assert result.exit_code == 0
    assert "Hello World 123" in result.output


def test_cli_remove_stopwords(runner):
    result = runner.invoke(
        cli,
        [
            "text",
            "remove-stopwords",
            "This is a test",
            "--stop-words",
            "is",
            "--stop-words",
            "a",
        ],
    )
    assert result.exit_code == 0
    assert "this test" in result.output


def test_cli_shuffle(runner):
    result = runner.invoke(
        cli, ["struct", "shuffle", "1", "2", "3", "4", "5", "--seed", "42"]
    )
    assert result.exit_code == 0
    assert "['4', '2', '3', '5', '1']" in result.output


def test_cli_flatten(runner):
    result = runner.invoke(cli, ["struct", "flatten", "[[1,2],[3,4],[5]]"])
    assert result.exit_code == 0
    assert "[1, 2, 3, 4, 5]" in result.output


def test_cli_unique(runner):
    result = runner.invoke(cli, ["struct", "unique", "1", "2", "2", "3", "1"])
    assert result.exit_code == 0
    assert "['1', '2', '3']" in result.output
