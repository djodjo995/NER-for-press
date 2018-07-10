import fr_core_news_md
from  config.config_dow_jones import avro_field_names
from src.custom_classes.entities import entity

nlp = fr_core_news_md.load()


def articles_generator(corpus):
    """
    :param corpus:
    :return: an article generator from the corpus
    """
    for article in corpus:
        yield corpus[article]


def get_spacy_entities_from_corpus(corpus):
    """
    :param corpus: extracted from avro files in DJ API.
    :return: dictionary of the entities contained in corpus.
    """
    list_entities = {}
    articles = articles_generator(corpus)
    for article in articles:
        corps_article = article[avro_field_names["Corps"]]
        id_article = article[avro_field_names["id_article"]]
        try:
            doc = nlp(corps_article)
            entities = doc.ents
            for ent in entities:
                entity_key = '%s (%s)' % (ent.text, ent.label_)
                if entity_key in list_entities.keys():
                    list_entities[entity_key].article.add(id_article)
                else:
                    ids_article = {id_article}
                    list_entities[entity_key] = entity(ent.text, ent.label_, ids_article)
        except MemoryError:
            print(u"memory error")
    return list_entities




