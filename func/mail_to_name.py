def get_firstname(sentence, names, names_threshold):
    '''Returns the name found in a string. If no name found returns None'''
    for firstname in names.loc[names.total>=names_threshold]["firstname"]:
        if firstname in sentence:
            return firstname