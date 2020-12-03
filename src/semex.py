import requests
import gensim
import nltk
import re

from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

from utils import download_nltk_packages
from utils import ROOTPATH, SRCPATH, DATAPATH

pos_tag_map = {
    "NN": [wordnet.NOUN],
    "JJ": [wordnet.ADJ, wordnet.ADJ_SAT],
    "RB": [wordnet.ADV],
    "VB": [wordnet.VERB],
}

validation_threshold = 0.25


def init_numberbatch(filepath: str = f"{DATAPATH}/numberbatch-en-19.08.txt"):
    return gensim.models.KeyedVectors.load_word2vec_format(filepath, binary=False)


def tokenize(string):
    return word_tokenize(string)


def pos_tag(tokens):
    return nltk.pos_tag(tokens)


def handle_stopwords(tokens):
    _stopwords = stopwords.words("english")
    results = []

    for token in tokens:
        if token[0].lower() not in _stopwords:
            results.append(tuple([token[0].lower(), token[1]]))

    return results


def convert_pos_tags(nltk_pos_tag):
    root_tag = nltk_pos_tag[0:2]

    try:
        pos_tag_map[root_tag]
        return pos_tag_map[root_tag]
    except KeyError:
        return ""


def get_synsets(tokens):
    synsets = {}

    for token in tokens:
        wn_pos_tag = convert_pos_tags(token[1])
        if wn_pos_tag == "":
            continue
        else:
            synsets[token[0]] = wordnet.synsets(token[0], wn_pos_tag)

    return synsets


def get_synset_tokens(validation_model, synsets_by_token):
    tokens = {}

    for token, synsets in synsets_by_token.items():
        for synset in synsets:
            sname = synset.name().split(".")[0]
            validation_score = 0
            try:
                validation_score = validation_model.similarity(token, sname)
            except KeyError:
                print(f"{sname} not in vocabuary")
            # print(f"{token}:{sname} = {validation_score}")
            if validation_score > validation_threshold:
                if sname in tokens:
                    tokens[sname] += 1
                else:
                    tokens[sname] = 1

    return tokens


def get_hypernyms(synsets_by_token):
    hypernyms = {}

    for token, synsets in synsets_by_token.items():
        _hypernyms = []
        for synset in synsets:
            for h in synset.hypernyms():
                _hypernyms.append(h)
        hypernyms[token] = _hypernyms

    return hypernyms


def get_hypernym_tokens(validation_model, hypernyms_by_token):
    tokens = {}

    for token, hypernyms in hypernyms_by_token.items():
        for hypernym in hypernyms:
            hname = hypernym.name().split(".")[0]
            validation_score = 0
            try:
                validation_score = validation_model.similarity(token, hname)
            except KeyError:
                print(f"{hname} not in vocabuary")
            # print(f"{token}:{hname} = {validation_score}")
            if validation_score > validation_threshold:
                if hname in tokens:
                    tokens[hname] += 1
                else:
                    tokens[hname] = 1
    return tokens


def replace_underscores(tokens):
    new_tokens = {}

    for key in tokens.keys():
        mod_key = re.sub(r"_", " ", key)
        new_tokens[mod_key] = tokens[key]

    return new_tokens


def expand_query(validation_model, query):
    # Preprocess, tag, and tokenize
    tokens = tokenize(query)
    tokens = pos_tag(tokens)
    tokens = handle_stopwords(tokens)

    # Get initial list of synsets
    synsets = get_synsets(tokens)

    # Tokenize and validate synonyms
    synonyms = get_synset_tokens(validation_model, synsets)
    synonyms = replace_underscores(synonyms)

    # Tokenize and validate hypernyms
    hypernyms = get_hypernyms(synsets)
    hypernyms = get_hypernym_tokens(validation_model, hypernyms)
    hypernyms = replace_underscores(hypernyms)

    return tokens, {**synonyms, **hypernyms}
