#Dataset Interface:
def getRow(index: int) -> tuple:
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

def retrieve(question: str) -> tuple:

    """
    :param question:
    :return: tuple
        docs: document idenitifiers for comparison
        chunks: actual retrieved chunks of text
    """
    docs: list = [] #doc IDs
    chunks: list = [str] #actual chunks of text

    #TODO: Add your interface code here:

    return docs, chunks

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
#Make sure you dedupe retrieved  and relevant documents

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
    assert denominator > 0, "zero denominator"

    return (2 * p * r) / denominator

def f1_at_k(retrieved: list, relevant: list, k: int) -> float:
    assert k > 0, "k must be greater than 0"
    return f1(retrieved[:k], relevant)


#TODO: Generation metrics (Requires LLM as judge)

#TODO: Run on dataset , Average metrics
