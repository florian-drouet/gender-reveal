import pandas as pd
from func.preprocess_insee_file import clean_insee_file, save_file

# original source : https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
insee_file = pd.read_csv("local_data/nat2020.csv", sep=';')

prenoms = clean_insee_file(insee_file=insee_file)
save_file(prenoms)
