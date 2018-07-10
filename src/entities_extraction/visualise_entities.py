def sort_ner_names_by_mentions(ner):
    """

    :param ner: list of entity objects.
    :return: list of entities names sorted by number of mentions. They are no longer objects.
    """
    return sorted(ner, key=lambda k: len(ner[k].article), reverse=True)


def ner_names_by_type(ner, type):
    """

    :param ner: list of entity objects.
    :param type: defined in config.
    :return: list of entity objects that are of the type of interest.
    """
    return {x: ner[x] for x in ner if (ner[x].type == type)}