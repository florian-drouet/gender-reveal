import pandas as pd
from func.preprocess_insee_file import clean_insee_file, save_file
from func.name_to_gender import get_gender_from_name
from func.text_preprocessing import TextPreprocessing

# original source : https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
insee_file = pd.read_csv("data/nat2020.csv", sep=';')

try:
    names = pd.read_csv('data/names.csv')
except:
    names = clean_insee_file(insee_file=insee_file)
    save_file(names)

gender = get_gender_from_name(name_to_classify='gaetan', names=names)

# test data
df = pd.DataFrame({'names': ["Alice", "Gaëtan", "Florian", "Clément", "Céline"]})

prenoms_clean = TextPreprocessing(serie=df.names)
df["prenoms_clean"] = prenoms_clean.lower().normalize().regex_cleaner().clean_whitespaces().serie

df["gender"] = df.prenoms_clean.apply(get_gender_from_name, names=names)

print(df)