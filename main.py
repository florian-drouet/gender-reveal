import pandas as pd
from pandas.io.parsers import read_csv
from func.preprocess_insee_file import clean_insee_file, save_file
from func.name_to_gender import get_gender_from_name
from func.mail_to_name import get_firstname
from func.text_preprocessing import TextPreprocessing, TextPreprocessingDataFrame

# original source : https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
insee_file = pd.read_csv("data/nat2020.csv", sep=";")

try:
    names = pd.read_csv("data/names.csv")
except:
    names = clean_insee_file(insee_file=insee_file)
    save_file(names)

# test data
#df = pd.DataFrame({"email_address": ["florian-drouet78-du92@gmail.com", "florian.drt-21.12@gmail.com", "julie.lescaut@orange.fr", "data.scientist@gmail.com"]})

df = pd.read_csv("/Users/floriandrouet/OneDrive - Health Hero/Documents/data_science/local_notebooks/local_data/monsherpa_mail_adresse.csv", header=None).rename(columns={0: 'email_address'})
df = df.sample(50, random_state=42)

splitted_emails = df.email_address.str.split("@", expand=True).rename(columns={0: "before_split", 1: "after_split"})

splitted_emails = splitted_emails.before_split.str.split(pat='\W+', expand=True)

to_clean = TextPreprocessingDataFrame(dataframe=splitted_emails)
first_split = (to_clean.lower().numbers_remover().clean_whitespaces().dataframe)
print(first_split)

## TODO before continuing make an == statement with names.csv if name is found the no doubt ! (will be faster and more accurate)
first_split_names = first_split.applymap(get_firstname, na_action='ignore', names=names, names_threshold=500)
#print(first_split_names)

# get gender from normalized names
first_split_names_genders = first_split_names.applymap(get_gender_from_name, na_action='ignore', threshold=95, names=names)

first_split_names_genders_results = first_split_names_genders.apply(pd.Series.value_counts, axis=1)[['male', 'female']].fillna(0)

df['proba_man_from_email'] = first_split_names_genders_results['male']
df['proba_female_from_email'] = first_split_names_genders_results['female']

df["gender"] = df.proba_man_from_email-df.proba_female_from_email

def infer_gender(value):
    if value > 0:
        return 'man'
    elif value < 0:
        return 'female'
    else:
        return None

df["gender"] = df["gender"].apply(infer_gender)

print(df)
