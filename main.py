import pandas as pd
from func.preprocess_insee_file import clean_insee_file, save_file
from func.name_to_gender import get_gender_from_name, infer_gender_from_proba_columns
from func.mail_to_name import get_firstname
from func.text_preprocessing import TextPreprocessingDataFrame
import datetime

begin_time = datetime.datetime.now()

# original source : https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
insee_file = pd.read_csv("data/nat2020.csv", sep=";")

try:
    names = pd.read_csv("data/names.csv")
except:
    names = clean_insee_file(insee_file=insee_file)
    save_file(names)

# test data
df = pd.DataFrame({"email_address": ["florian-drouet78-du92@gmail.com", "florian.drt-21.12@gmail.com", "julie.lescaut@orange.fr", "data.scientist@gmail.com"]})

# split all emails at '@'
df_splitted_emails = df.email_address.str.split("@", expand=True).rename(columns={0: "before_split", 1: "after_split"})
# regex split emails on characters like ",.-_" with expansion
df_splitted_emails = df_splitted_emails.before_split.str.split(pat='\W+', expand=True)

# cleaning dataframe and trying to get firstnames
to_clean = TextPreprocessingDataFrame(dataframe=df_splitted_emails)
df_first_split = (to_clean.lower().numbers_remover().clean_whitespaces().dataframe)
df_first_split_names = df_first_split.applymap(get_firstname, na_action='ignore', names=names)

# get gender from normalized names
df_first_split_names_genders = df_first_split_names.applymap(get_gender_from_name, na_action='ignore', threshold=95, names=names)
df_first_split_names_genders_results = df_first_split_names_genders.apply(pd.Series.value_counts, axis=1)[['male', 'female']].fillna(0)

df['proba_man_from_email'] = df_first_split_names_genders_results['male']
df['proba_female_from_email'] = df_first_split_names_genders_results['female']

# get most probable gender
df["gender"] = df.proba_man_from_email-df.proba_female_from_email
df["gender"] = df["gender"].apply(infer_gender_from_proba_columns)

#df.to_csv("gender_from_mail_qare.csv", index=False, encoding='utf-8')

print(df)
print(datetime.datetime.now() - begin_time)
