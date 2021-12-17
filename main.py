import pandas as pd
from func.preprocess_insee_file import clean_insee_file, save_file
from func.name_to_gender import get_gender_from_name
from func.mail_to_name import get_firstname
from func.text_preprocessing import TextPreprocessing

# original source : https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
insee_file = pd.read_csv("data/nat2020.csv", sep=";")

try:
    names = pd.read_csv("data/names.csv")
except:
    names = clean_insee_file(insee_file=insee_file)
    save_file(names)

# test data
df = pd.DataFrame({"email_address": ["florian-drt2.1@gmail.com"]})

splitted_emails = df.email_address.str.split("@", expand=True).rename(columns={0: "before_split", 1: "after_split"})

to_clean = TextPreprocessing(serie=splitted_emails.before_split)
splitted_emails["before_split_clean"] = (to_clean.lower().normalize().regex_cleaner().numbers_remover().clean_whitespaces().serie)

splitted_emails["firstname"] = splitted_emails.before_split_clean.apply(get_firstname, names=names, names_threshold=500)

# clean and normalize names
firstname_clean = TextPreprocessing(serie=splitted_emails.firstname)
df["firstname_clean"] = (firstname_clean.lower().normalize().regex_cleaner().clean_whitespaces().serie)

# get gender from normalized names
df["gender_from_name"] = df.firstname_clean.apply(get_gender_from_name, threshold=95, names=names)

print(df)
