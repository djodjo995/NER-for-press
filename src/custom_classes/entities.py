
from src.clean_entites.gestion_contextes import get_context



class entity:
    def __init__(self, nom, type, article):
        self.nom = nom
        self.type = type
        self.article = article
        self.contextes = []
        self.entites_cooccurrentes = {}


    def add_contexte(self, corpus_entity, sentences_nb):
        self.contextes = get_context(self, corpus_entity, sentences_nb)

