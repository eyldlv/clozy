import spacy

nlp = spacy.load('de_core_news_sm', exclude=['ner'], disable=['parser'])