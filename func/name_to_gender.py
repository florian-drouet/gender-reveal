#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def get_gender_from_name(
    name_to_classify: str, threshold: int, names: pd.DataFrame
) -> str:
    proba_man = names.loc[(names.firstname == name_to_classify)]["proba_man"].values
    if proba_man >= threshold:
        return "male"
    elif proba_man <= 100 - threshold:
        return "female"
    else:
        return "unclear"

def infer_gender_from_proba_columns(value: int) -> str:
    if value > 0:
        return 'male'
    elif value < 0:
        return 'female'
    else:
        return None