#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def get_gender_from_name(
    name_to_classify: str, threshold: int, names: pd.DataFrame
) -> str:
    proba_homme = names.loc[(names.prenom == name_to_classify)]["proba_homme"].values
    if proba_homme >= threshold:
        return "male"
    elif proba_homme <= 100 - threshold:
        return "female"
    else:
        return "unclear"