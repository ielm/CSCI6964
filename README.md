# Semantic Query-Expansion for Document Retrieval With Dense Word Embedding Validation

Homework 2 for CSCI 6964 (Information Retrieval). This was written and tested on MacOS, but any unix system should work .

# Installation
Assuming you are using a Unix-like OS, the homework can be run as follows. Windows users, sorry... Proceed at your own peril.

## Installing SOLR

Assuming you are in the root directory of the project, simply run the following to extract the tar file:
```bash
tar -zxf solr-8.6.0.tgz
```

Running Solr is easy.
```bash
cd solr-8.6.0

bin/solr start
```

## Dependencies

 * [Python 3.8](https://docs.python.org/3.8/)
 * [NLTK](https://www.nltk.org/)
 * [gensim](https://radimrehurek.com/gensim/)

To install dependencies, run the following:

```bash
pip install -r requirements.txt
```


In order to download all required NLTK packages, run the following from the root directory of the project: 

```bash
python src/utils.py
```

## Running the homework 

You can run the full homework code with the following line: 

```bash
python src/main.py
``` 

## Directory Structure

 * Project code is in `src` directory.
 * Data is in `data` directory.
 * Results are in the `results` directory.

---

# How it works

The semantic query expansion process is conceptually simple. The basic steps are as follows:

1. The query is tokenized and tagged by each token's part of speech. 
2. Stopwords and extraneous parts of speech are removed for a cleaner query sample.
3. Each token is disambiguated so there are no multiply included words. 
4. Synonym and hypernym sets are extracted for each token using WordNet. 
5. Each tokenized synonym and hypernym is validated by computing a similarity score between the original token word and the synonym/hypernym. Synonyms and hypernyms below a threshold similarity score are discarded. 



