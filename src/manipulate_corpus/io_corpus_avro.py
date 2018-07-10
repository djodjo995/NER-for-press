import os
from config.config_dow_jones import avro_field_names
from avro.datafile import DataFileReader
from avro.io import DatumReader


def read_corpus(corpus_path):
    avro_files_path = [os.path.join(corpus_path, filename) for filename in os.listdir(corpus_path) if
                       os.path.splitext(filename)[1] == '.avro']
    for avro_file in avro_files_path:
        small_corpus = DataFileReader(open(avro_file, 'rb'), DatumReader())
        for article in small_corpus:
            yield article


def construct_corpus(corpus_path):
    return {article[avro_field_names['id_article']]: article for article in read_corpus(corpus_path)}