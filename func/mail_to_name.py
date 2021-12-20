import pandas as pd

def get_firstname(sentence: str, names: pd.DataFrame) -> str:
    '''
    First, check if the sentence has an equal matching firstname
    If no equal matching, check if we can find a firstname in sentence
    Returns: a firstname or None
    '''
    for firstname in names["firstname"]:
        if firstname == sentence:
            return firstname
    for firstname in names["firstname"]:
        if firstname in sentence:
            return firstname