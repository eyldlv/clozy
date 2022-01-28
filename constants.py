# clozy v. 0.0.1
# Constants module

# Author: Eyal Dolev
# Matricuation number: 20-713-897
# Date: 30.05.2021


# load the small SpaCy German model
import spacy

nlp = spacy.load('de_core_news_sm', exclude=['ner'], disable=['parser'])