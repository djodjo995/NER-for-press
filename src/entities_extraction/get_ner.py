import numpy as np
import pandas as pd
from src.clean_entites.gestion_contextes import *
from src.entities_extraction.spacy_entities_ner import get_spacy_entities_from_corpus

def remove_entities_that_are_not_entities(raw_entities, corpus):
    #TODO
    return raw_entities


def get_entities(corpus, ner_package):
    if ner_package == 'spacy':
        raw_entities = get_spacy_entities_from_corpus(corpus)
    elif ner_package == 'google nlp':
        raw_entities = get_google_entities_from_corpus()
    cleaned_entities = remove_entities_that_are_not_entities(raw_entities, corpus)
    return cleaned_entities

def clean_corpus(corpus):
    """
    :param corpus: the corpus from which we want to remove unwanted strings
    :return: clean corpus
    """
    for c in corpus:
        corpus[c]['body'] = corpus[c]['body'].replace('\xa0', ' ').replace('\n\n', '').replace('  ', ' ')

    return corpus


def get_corpus(entity, corpus):
    """
    :param entity:
    :param corpus:
    :return: corpus of articles containing the entity, identified by entity.article
    """
    ids = entity.article
    return {id: corpus[id] for id in ids}


def create_inverse_dictionary(entities):
    articles = {}
    for ent in entities:
        for j in entities[ent].article:
            try:
                articles[j].add(entities[ent])
            except KeyError:
                articles[j] = {entities[ent]}
    return articles


def add_cooccurrence_from_dictionary(entities, articles):
    """
    :param entities: entities to which we add their co-occurrent entities
    :param articles: inverse dictionary : articles are the keys, entities are the values
    :return: entities with their co-occurrente entities, which belong to the entity class
    """
    for ent in entities:
        for j in entities[ent].article:
            entities[ent].entites_cooccurrentes = articles[j]
        entities[ent].entites_cooccurrentes.remove(entities[ent])
    return entities


def add_cooccurrence(entities):
    articles = create_inverse_dictionary(entities)
    entities = add_cooccurrence_from_dictionary(entities, articles)
    return entities


def enrich_entities(cleaned_entities, corpus, sentences_nb):
    enriched_entities = cleaned_entities.copy()
    for entity in enriched_entities:
        corpus_entity = get_corpus(enriched_entities[entity], corpus)
        enriched_entities[entity].add_contexte(corpus_entity, sentences_nb)
    enriched_entities = add_cooccurrence(enriched_entities)
    return enriched_entities


def get_ner(corpus, sentences_nb):
    corpus = clean_corpus(corpus)
    cleaned_entities = get_entities(corpus, "spacy")
    enriched_entities = enrich_entities(cleaned_entities, corpus, sentences_nb)
    return enriched_entities


