class TextPreprocessing:
    def __init__(self, serie):
        self.serie = serie

    def lower(self):
        self.serie = self.serie.str.lower()
        return self

    def normalize(self):
        self.serie = (
            self.serie.str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        return self

    def regex_cleaner(self):
        self.serie = self.serie.str.replace("[^\w\s]", " ", regex=True)
        return self
    
    @staticmethod
    def nb_rmv(sentence):
        return ''.join([character for character in sentence if not character.isdigit()])
    
    def numbers_remover(self):
        self.serie = self.serie.apply(self.nb_rmv)
        return self

    @staticmethod
    def cln_whtspcs(sentence):
        if sentence is None:
            return None
        else:
            return " ".join(str(sentence).split())

    def clean_whitespaces(self):
        self.serie = self.serie.apply(self.cln_whtspcs)
        return self
