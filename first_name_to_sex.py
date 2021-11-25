#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import unidecode

def delete_accent(word: str) -> str:
    """Delete accents in a string"""
    return unidecode.unidecode(word)

def check_sex(sex: str) -> str:
    """Checks the sex of a person and returns 'indetermine' if the sex can be both male and female"""
    if sex == 'm,f' or sex == 'f,m':
        return "indetermine"
    else:
        return sex
    
def make_dictionary(dataframe):
    """
    Input : Prenom.csv as a pandas dataframe
    Output : a python dictionary {"PRENOM: SEX"}
    """
    
    # Type of objects in the two first columns is string and we apply preprocessing functions
    dataframe['01_prenom']=dataframe['01_prenom'].apply(lambda x: str(x))
    dataframe["02_genre"]=dataframe["02_genre"].apply(lambda x: str(x))
    dataframe['01_prenom']=dataframe['01_prenom'].apply(delete_accent)
    dataframe["02_genre"]=dataframe["02_genre"].apply(check_sex)

    # We return the two first table into a dictionary {"PRENOM: SEX"}
    return dict([(i,a) for i, a in zip(dataframe["01_prenom"], dataframe["02_genre"])])

def get_sex_from_name(liste_name_test: list, first_name_table: dict) -> list:
    """
    Input : the first names as a python list
    Output : the corresponding sexes as a python list. If the first name is not found in the dictionary then it will add
    'Indetermine' to the list.
    """
    column_sex = []
    for index, prenom in enumerate(liste_name_test):
        try:
            column_sex.append(first_name_table[delete_accent(liste_name_test[index].lower())])
        except:
            column_sex.append("indetermine")
    return column_sex

if __name__ == '__main__':
    # the file Prenoms.csv in ANSI encoded
    df = pd.read_csv("Prenoms.csv", sep=";", encoding='ANSI')
    first_name_table = make_dictionary(df)
    dict_vocabulary = {"m": "male", "f": "female", "indetermine": "unclear"}
    while True:
        name = input('Enter your name:')
        liste_name_test = [name]
        column_sex = get_sex_from_name(liste_name_test, first_name_table)
        print("Your gender is : "+str(dict_vocabulary[column_sex[0]])+"\n")