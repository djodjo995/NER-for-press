import re
import datetime

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Je|Tu|Il|Elle|Ils|Elles|On|But\s|However\s|That\s|This\s|Wherever)F"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences



def get_context_per_article(entity, article, sentences_nb):
    date = datetime.datetime.utcfromtimestamp(article['publication_datetime'] / 1000)
    sentences = split_into_sentences(article['body'].replace("\n\n", ""))
    c = []
    for i in range(0, len(sentences)):
        if entity.nom in sentences[i]:
            for j in range(max(i - sentences_nb, 0), i):
                c.append(sentences[j])
            c.append(sentences[i])
            for j in range(i, min(i + sentences_nb, len(sentences) - 1)):
                c.append(sentences[j])
    seen = set()
    c = [x for x in c if not (x in seen or seen.add(x))]
    contexts = [" ".join(c)]
    return list(
        set([(context, article['title'], date.strftime('%Y-%m-%d'), article['an']) for context in contexts]))


def get_context(entity, corpus_entity, sentences_nb):
    contextes = [get_context_per_article(entity, corpus_entity[a], sentences_nb) for a in entity.article]
    return contextes
