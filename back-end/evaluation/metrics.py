#Dataset Interface:
import math
import statistics


def getRow(index: int, table) -> tuple:
    """
    :param index: int (row number)
    :returns: tuple:
        question: str : question from the dataset
        answer: str : correct answer from the dataset
        ground_truth: list[str] : list of ground truth phrases from the dataset
        relevant_docs: list[Any] : list of document identifiers from the dataset
    """

    question: str = ""
    answer: str = ""
    ground_truth: list[str] = []
    relevant_docs: list = []

    #TODO: Add your interface code here:


    return question, answer, ground_truth, relevant_docs

#RAG interface:
def generate(question: str) -> tuple:
    """

    :param question:
    :return: tuple
        docs: document identifiers for comparison
        chunks: actual retrieved chunks of text
        answer: RAG generated answer

    """
    docs: list = [] #doc IDs
    chunks: list = [str] #actual chunks of text
    answer: str = "" #generated answer

    #TODO: Add your interface code here:

    return docs, chunks, answer

#retrieval metrics:

def precision(retrieved: list, relevant: list) -> float:
    if len(retrieved) == 0: return 0
    if len(relevant) == 0: return 0

    true_positive: int = 0
    for i in retrieved:
        if i in relevant:
            true_positive += 1

    return true_positive / len(retrieved)

def precision_at_k(retrieved: list, relevant: list, k: int) -> float:
    assert k > 0, "k must be greater than 0"
    return precision(retrieved[:k], relevant)

def recall(retrieved: list, relevant: list) -> float:
    if len(retrieved) == 0: return 0
    if len(relevant) == 0: return 1

    true_positive: int = 0
    for i in retrieved:
        if i in relevant:
            true_positive += 1

    return true_positive/len(relevant)

def recall_at_k(retrieved: list, relevant: list, k: int) -> float:
    assert k>0, "k must be greater than 0"
    return recall(retrieved[:k], relevant)

def f1(retrieved: list, relevant: list) -> float:
    p = precision(retrieved, relevant)
    r = recall(retrieved, relevant)

    denominator = p + r
    if denominator == 0:
        return 0

    return (2 * p * r) / denominator

def f1_at_k(retrieved: list, relevant: list, k: int) -> float:
    assert k > 0, "k must be greater than 0"
    return f1(retrieved[:k], relevant)

#generation metrics:
def accuracy(generated: str, correct: str):
    return 0
def relevance(generated: str, ground_truth: list):
    return 0
def groundedness(generated: str, retrieved: list):
    return 0

#running eval:
def eval_row(index: int, table):

    question, correct_answer, ground_truth, relevant_docs = getRow(index, table)

    retrieved_docs, retrieved_chunks, generated_answer = generate(question)

    #retrieval metrics:

    p = precision(retrieved_docs, relevant_docs)
    p_at_k = [precision_at_k(retrieved_docs, relevant_docs, i+1) for i in range(len(retrieved_docs))]

    r = recall(retrieved_docs, relevant_docs)
    r_at_k = [recall_at_k(retrieved_docs, relevant_docs, i+1) for i in range(len(retrieved_docs))]

    f = f1(retrieved_docs, relevant_docs)
    f_at_k = r_at_k = [f1_at_k(retrieved_docs, relevant_docs, i+1) for i in range(len(retrieved_docs))]

    #generation metrics:

    a = accuracy(generated_answer, correct_answer)
    rel = relevance(generated_answer, ground_truth)
    g = groundedness(generated_answer, retrieved_chunks)

    #return:
    return {
        "precision": p,
        "precision_at_k": p_at_k,
        "recall": r,
        "recall_at_k": r_at_k,
        "f1_score": f,
        "f1_score_at_k": f_at_k,
        "accuracy": a,
        "relevance": rel,
        "groundedness": g
    }

def eval(table):
    metrics = [eval_row(i, table) for i in range(len(table))]
    return metrics

if __name__ == "__main__":
    #your code here:

    #get dataset table / df:
    table = None

    results: list[dict] = eval(table)

    #do whatever you need to with the results here
    mean_recall = statistics.mean([result["recall"] for result in results])
    mean_accuracy = statistics.mean([result["accuracy"] for result in results])
    mean_relevance = statistics.mean([result["relevance"] for result in results])
    mean_groundedness= statistics.mean([result["groundedness"] for result in results])
    mean_recall_at_1 = statistics.mean([result["recall_at_k"][0] for result in results])

    #idk send them somewhere I guess?

    exit(0)