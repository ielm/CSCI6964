import subprocess
import nltk
import os

from pathlib import Path


ROOTPATH = f"{Path(os.getcwd())}"
SRCPATH = f"{ROOTPATH}/src"
DATAPATH = f"{ROOTPATH}/data"
RESULTSPATH = f"{ROOTPATH}/results"
TRECPATH = f"{RESULTSPATH}/trec_eval"


def print_homework_header():
    print(
        f"*******************************************************************\n"
        f"*                                                                 *\n"
        f"*  Semantic Query Expansion With Dense Word Embedding Validation  *\n"
        f"*                                                                 *\n"
        f"*  CSCI 6964 Homework 2 - Ivan Leon                               *\n"
        f"*                                                                 *\n"
        f"*******************************************************************\n"
    )


def download_nltk_packages():
    nltk.download("wordnet")
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")


def readfile(filename):
    contents = None
    with open(filename, "r") as f:
        contents = f.read()
    return contents


def trec_eval(trec, ground_truth, solr_results):
    args = f"{trec} -q {ground_truth} {solr_results}".split()

    popen = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)
    popen.wait()
    output = popen.stdout.read()
    popen.stdout.close()

    return output


if __name__ == "__main__":
    download_nltk_packages()
