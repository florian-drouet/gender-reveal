import pandas as pd
import numpy as np
from func.text_preprocessing import TextPreprocessing


def clean_insee_file(insee_file):

    to_clean = TextPreprocessing(serie=insee_file.preusuel)
    insee_file["preusuel_clean"] = (
        to_clean.lower().normalize().regex_cleaner().clean_whitespaces().serie
    )

    prenoms = (
        insee_file[["preusuel_clean", "sexe", "nombre"]]
        .groupby(by=["preusuel_clean", "sexe"])
        .sum()
        .reset_index()
    )

    firstnames_clean = (
        pd.pivot_table(
            prenoms,
            values="nombre",
            index=["preusuel_clean"],
            columns=["sexe"],
            aggfunc=np.sum,
        )
        .reset_index()
        .fillna(0.0)
    )
    firstnames_clean = firstnames_clean.rename(
        columns={"preusuel_clean": "firstname", 1: "proba_man", 2: "proba_female"}
    )

    firstnames_clean["total"] = firstnames_clean.proba_man + firstnames_clean.proba_female
    firstnames_clean["proba_man"] = round(
        firstnames_clean.proba_man.div(firstnames_clean.total).mul(100), 2
    )
    firstnames_clean["proba_female"] = round(
        firstnames_clean.proba_female.div(firstnames_clean.total).mul(100), 2
    )

    firstnames_clean["firstname_length"] = firstnames_clean.firstname.str.len()

    # Two parameters here : first_length min is set to 3 (no firstnames with less than 3 letters) and
    # the 'popularity' of the firstname is set to at least 1000 occurences
    firstnames_clean = firstnames_clean.loc[(firstnames_clean.firstname_length>=3) & (firstnames_clean.total>=1000)].dropna()

    return firstnames_clean[["firstname", "firstname_length", "proba_man", "proba_female", "total"]].sort_values(by=["firstname_length", "total"], ascending=False).reset_index(drop=True)


def save_file(file):
    file.to_csv("data/names.csv", index=False, encoding="utf-8")
