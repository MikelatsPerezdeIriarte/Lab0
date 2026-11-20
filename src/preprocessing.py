"""Functions for preprocessing data"""

import math
import random
import re


def remove_missing(values: list) -> list:
    """Removes missing values from a list of strings."""
    missing = {None, "", "nan"}
    return [v for v in values if v not in missing]


def fill_missing(values: list, fill_value=0) -> list:
    """Fills the missing values with a default value (0 by default)."""
    missing = {None, "", "nan"}
    return [fill_value if v in missing else v for v in values]


def remove_duplicates(values: list) -> list:
    """Removes duplicates from a list of values."""
    return list(dict.fromkeys(values))


def normalize(values: list, new_min: float = 0.0, new_max: float = 1.0) -> list:
    """Normalizes a list of numerical values to the range [new_min, new_max]."""
    if not values:
        return []
    min_val, max_val = min(values), max(values)
    if max_val == min_val:
        return [new_min] * len(values)
    return [
        ((v - min_val) / (max_val - min_val)) * (new_max - new_min) + new_min
        for v in values
    ]


def standardize(values: list) -> list:
    """Standarizes a list of numerical values (z-score)."""
    if not values:
        return []
    mean = sum(values) / len(values)
    std_dev = math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))
    if std_dev == 0:
        return [0.0] * len(values)
    return [(v - mean) / std_dev for v in values]


def clip(values: list, min_val: float, max_val: float) -> list:
    """Clips a list of numerical values to the range [min_val, max_val]"""
    return [max(min_val, min(v, max_val)) for v in values]


def to_integers(values: list) -> list:
    """Converts a list of strings to integers"""
    result = []
    for v in values:
        try:
            result.append(int(v))
        except (ValueError, TypeError):
            continue
    return result


def log_transform(values: list) -> list:
    """Converts a list of numeric values to logarithmic scale"""
    return [math.log(v) for v in values if v > 0]


def tokenize(text: str) -> list:
    """Tokenizes a text into words selecting only alphanumeric characters and lower-casing words."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def remove_punctuation(text: str) -> str:
    """Removes the punctuation from a text."""
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def remove_stopwords(text: str, stop_words: list) -> str:
    """Removes stopwords from a text."""
    stop_set = set(w.lower() for w in stop_words)
    words = text.lower().split()
    return " ".join(w for w in words if w not in stop_set)


def flatten(nested_list: list) -> list:
    """Flattens a list of lists."""
    return [item for sublist in nested_list for item in sublist]


def shuffle(values: list, seed: int = None) -> list:
    """Shuffles a list of values with an optional seed."""
    values_copy = values.copy()
    random.seed(seed)
    random.shuffle(values_copy)
    return values_copy
