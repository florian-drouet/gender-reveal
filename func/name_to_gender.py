#!/usr/bin/env python
# coding: utf-8

def get_gender_from_name(name_to_classify, names):
    proba_homme = names.loc[(names.prenom==name_to_classify)]['proba_homme'].values
    if proba_homme >= 95:
        return 'male'
    elif proba_homme <= 5:
        return 'female'
    else:
        return 'unclear'