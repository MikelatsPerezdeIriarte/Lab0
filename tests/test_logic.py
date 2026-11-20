import math

import pytest
from src import preprocessing as pp


@pytest.fixture
def sample_numbers():
    """A list of numbers to use in various tests."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_text():
    return "Hello, World! This is a test."


def test_remove_missing():
    assert pp.remove_missing([1, None, 2, "", "nan", 3]) == [1, 2, 3]
    assert pp.remove_missing([]) == []


def test_fill_missing():
    assert pp.fill_missing([1, None, 2, "", "nan", 3], 0) == [1, 0, 2, 0, 0, 3]
    assert pp.fill_missing([1, None, 2], 99) == [1, 99, 2]


@pytest.mark.parametrize(
    "input_list, expected",
    [
        ([1, 2, 2, 3, 1], [1, 2, 3]),
        (["a", "b", "a", "c"], ["a", "b", "c"]),
        ([], []),
    ],
)
def test_remove_duplicates(input_list, expected):
    assert pp.remove_duplicates(input_list) == expected


@pytest.mark.parametrize(
    "values, new_min, new_max, expected",
    [
        ([0, 5, 10], 0.0, 1.0, [0.0, 0.5, 1.0]),
        ([1, 2, 3], 10.0, 20.0, [10.0, 15.0, 20.0]),
        ([5, 5, 5], 0.0, 1.0, [0.0, 0.0, 0.0]),
    ],
)
def test_normalize(values, new_min, new_max, expected):
    result = pp.normalize(values, new_min, new_max)
    assert result == pytest.approx(expected)


def test_normalize_default():
    result = pp.normalize([0, 5, 10])
    assert result == pytest.approx([0.0, 0.5, 1.0])


def test_standardize(sample_numbers):
    expected = [(x - 3) / math.sqrt(2) for x in sample_numbers]
    result = pp.standardize(sample_numbers)
    assert result == pytest.approx(expected)


def test_standardize_constant():
    assert pp.standardize([5, 5, 5]) == [0.0, 0.0, 0.0]


def test_clip():
    assert pp.clip([1, 2, 3, 4, 5], 2, 4) == [2, 2, 3, 4, 4]
    assert pp.clip([-1, 0, 1], 0, 1) == [0, 0, 1]


def test_to_integers():
    assert pp.to_integers(["1", "2", "abc", "3.5", "4"]) == [1, 2, 4]
    assert pp.to_integers(["a", "b"]) == []


def test_log_transform():
    values = [1, math.e, 10, 0, -5]
    expected = [0.0, 1.0, math.log(10)]
    result = pp.log_transform(values)
    assert result == pytest.approx(expected)


def test_tokenize():
    text = "Hello, World! 123"
    assert pp.tokenize(text) == ["hello", "world", "123"]
    assert pp.tokenize("") == []


def test_remove_punctuation():
    text = "Hello, World! 123"
    assert pp.remove_punctuation(text) == "Hello World 123"
    assert pp.remove_punctuation("") == ""


def test_remove_stopwords():
    text = "This is a test"
    stop_words = ["is", "a"]
    assert pp.remove_stopwords(text, stop_words) == "this test"
    assert pp.remove_stopwords("Hello World", []) == "hello world"


def test_flatten():
    assert pp.flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert pp.flatten([]) == []
    assert pp.flatten([[], [1], []]) == [1]


def test_shuffle():
    values = [1, 2, 3, 4, 5]
    shuffled1 = pp.shuffle(values, seed=42)
    shuffled2 = pp.shuffle(values, seed=42)
    assert shuffled1 == shuffled2
    original = values.copy()
    pp.shuffle(values, seed=None)
    assert values == original
    assert sorted(shuffled1) == sorted(values)
