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

    prenoms_clean = (
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
    prenoms_clean = prenoms_clean.rename(
        columns={"preusuel_clean": "prenom", 1: "proba_homme", 2: "proba_femme"}
    )

    prenoms_clean["tot"] = prenoms_clean.proba_homme + prenoms_clean.proba_femme
    prenoms_clean["proba_homme"] = round(
        prenoms_clean.proba_homme.div(prenoms_clean.tot).mul(100), 2
    )
    prenoms_clean["proba_femme"] = round(
        prenoms_clean.proba_femme.div(prenoms_clean.tot).mul(100), 2
    )

    return prenoms_clean[["prenom", "proba_homme", "proba_femme"]]


def save_file(file):
    file.to_csv("data/prenoms.csv", index=False, encoding="utf-8")
