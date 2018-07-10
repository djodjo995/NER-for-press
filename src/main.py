from src.manipulate_corpus.io_corpus_avro import read_corpus


def get_entities_from_corpus(corpus_path):
    article_iterator = read_corpus(corpus_path=corpus_path)
