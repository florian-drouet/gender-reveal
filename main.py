import pandas as pd
from func.preprocess_insee_file import clean_insee_file, save_file
from func.name_to_gender import get_gender_from_name
from func.text_preprocessing import TextPreprocessing

# original source : https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
insee_file = pd.read_csv("data/nat2020.csv", sep=";")

try:
    names = pd.read_csv("data/names.csv")
except:
    names = clean_insee_file(insee_file=insee_file)
    save_file(names)

# test data
df = pd.DataFrame({"firstnames": ["Alice", "Gaëtan", "Florian", "Clément", "Céline"]})

# clean and normalize names
firstnames_clean = TextPreprocessing(serie=df.firstnames)
df["firstnames_clean"] = (
    firstnames_clean.lower().normalize().regex_cleaner().clean_whitespaces().serie
)

# get gender from normalized names
df["gender_from_name"] = df.firstnames_clean.apply(
    get_gender_from_name, threshold=95, names=names
)

print(df)
