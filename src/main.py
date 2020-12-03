import urllib.parse
import codecs
from solr import SOLR
from semex import init_numberbatch, expand_query
from utils import print_homework_header, readfile, trec_eval
from utils import ROOTPATH, SRCPATH, DATAPATH, TRECPATH, RESULTSPATH


# Solr parameters
port = "8983"
collection = "trec"
fileNumber = 100

# Trec parameter
IRModel = "DFR"


def get_queries(filepath=f"{DATAPATH}/queries.txt"):
    q_id = []
    q_text = []

    with codecs.open(filepath, "r", "UTF-8") as file:
        for line in file:
            elements = line.split(":::")
            q_id.append(elements[0])
            q_text.append(elements[1])

    return q_id, q_text


def run_baseline(solr):
    fields = ["docno", "score"]

    with codecs.open("results/baselineResults.txt", "w", "UTF-8") as file:
        q_id, q_text = get_queries()
        for id_num, query in zip(q_id, q_text):
            print(f"Running query: {id_num}")
            query = urllib.parse.quote(query)

            results = solr.query(query=query, fields=fields, rows=15, sort="score asc")
            rank = 1
            for result in results:
                print(f"Num: {result['docno']}   \tScore: {result['score']}")
                file.write(
                    id_num
                    + " "
                    + "Q0"
                    + " "
                    + (str(result["docno"]))
                    .replace("'", "")
                    .replace("[", "")
                    .replace("]", "")
                    + " "
                    + str(rank)
                    + " "
                    + str(result["score"])
                    + " "
                    + IRModel
                    + "\n"
                )
                rank += 1


def run_expansion(validation_model, solr):
    fields = ["docno", "score"]

    with codecs.open("results/expansionResults.txt", "w", "UTF-8") as file:
        q_id, q_text = get_queries()
        for id_num, query in zip(q_id, q_text):
            print(f"Running query: {id_num}")

            _, expansion = expand_query(validation_model, query)

            query = urllib.parse.quote(f"{' '.join(expansion.keys())}")

            results = solr.query(query=query, fields=fields, rows=15, sort="score asc")
            rank = 1
            for result in results:
                print(f"Num: {result['docno']}   \tScore: {result['score']}")
                file.write(
                    id_num
                    + " "
                    + "Q0"
                    + " "
                    + (str(result["docno"]))
                    .replace("'", "")
                    .replace("[", "")
                    .replace("]", "")
                    + " "
                    + str(rank)
                    + " "
                    + str(result["score"])
                    + " "
                    + IRModel
                    + "\n"
                )
                rank += 1


def run_combined(validation_model, solr):
    fields = ["docno", "score"]

    with codecs.open("results/combinedResults.txt", "w", "UTF-8") as file:
        q_id, q_text = get_queries()
        for id_num, query in zip(q_id, q_text):
            print(f"Running query: {id_num}")

            _, expansion = expand_query(validation_model, query)

            query = urllib.parse.quote(f"{query} {' '.join(expansion.keys())}")

            results = solr.query(query=query, fields=fields, rows=15, sort="score asc")
            rank = 1
            for result in results:
                print(f"Num: {result['docno']}   \tScore: {result['score']}")
                file.write(
                    id_num
                    + " "
                    + "Q0"
                    + " "
                    + (str(result["docno"]))
                    .replace("'", "")
                    .replace("[", "")
                    .replace("]", "")
                    + " "
                    + str(rank)
                    + " "
                    + str(result["score"])
                    + " "
                    + IRModel
                    + "\n"
                )
                rank += 1


def evaluate():
    baseline_evaluation = trec_eval(
        f"{SRCPATH}/trec_eval",
        f"{TRECPATH}/groundTruth.txt",
        f"{RESULTSPATH}/baselineResults.txt",
    )

    with codecs.open(f"{TRECPATH}/baselineEvaluation.txt", "w", "UTF-8") as base:
        base.write(baseline_evaluation)

    expansion_evaluation = trec_eval(
        f"{SRCPATH}/trec_eval",
        f"{TRECPATH}/groundTruth.txt",
        f"{RESULTSPATH}/expansionResults.txt",
    )

    with codecs.open(f"{TRECPATH}/expansionEvaluation.txt", "w", "UTF-8") as expanded:
        expanded.write(expansion_evaluation)

    combined_evaluation = trec_eval(
        f"{SRCPATH}/trec_eval",
        f"{TRECPATH}/groundTruth.txt",
        f"{RESULTSPATH}/combinedResults.txt",
    )

    with codecs.open(f"{TRECPATH}/combinedEvaluation.txt", "w", "UTF-8") as combined:
        combined.write(combined_evaluation)


def main():
    print_homework_header()

    solr = SOLR()

    print("Loading ConceptNet NumberBatch model for semantic validation.")
    validation_model = init_numberbatch()
    print("ConceptNet NumberBatch loading finished!")

    run_baseline(solr)
    run_expansion(validation_model, solr)
    run_combined(validation_model, solr)

    evaluate()


if __name__ == "__main__":
    main()
