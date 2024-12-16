import csv
import json
from RAG_Core import PDFRAGSystem
import os
import sys
import tqdm
import openai

client = openai.OpenAI

accuracy_prompt = """ 
You are tasked with evaluating the accuracy of a response generated by an AI model. You will be provided with the following: 
A question.
The AI-generated answer to the question.
A human-labeled, correct answer to the same question.
Your goal is to assign an accuracy score between 0 and 5 based on how well the AI-generated answer aligns with the human-labeled answer. Use the following scoring criteria:
5: The AI-generated answer is completely accurate, comprehensive, and matches the human-labeled answer in all essential details.
4: The AI-generated answer is mostly accurate but may have minor omissions or slightly less clarity compared to the human-labeled answer.
3: The AI-generated answer is partially accurate but contains significant omissions or inaccuracies while still capturing some key aspects of the human-labeled answer.
2: The AI-generated answer has minimal alignment with the human-labeled answer and misses most key points, though it may contain a small amount of relevant information.
1: The AI-generated answer is largely incorrect, irrelevant, or incomplete, with only a trace of alignment to the human-labeled answer.
0: The AI-generated answer is entirely incorrect, irrelevant, or nonsensical.
Please respond with a single integer between 0 and 5, which is your score. Do not add any text before the score no matter what.
Here is your input:
"""
def accuracy(question: str, generated: str, answer: str) -> float:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": accuracy_prompt
            },
            {
                "role": "user",
                "content": "original question:" + question + "\n llm generated answer: " + generated + "\n human labeled answer" + answer
            }
        ]
    )
    try:
        accuracy = int(response.choices[0].message.content[0])
    except:
        print("error")
        accuracy = -1
    return accuracy / 5


relevance_prompt = """
You are an AI assistant tasked with evaluating the relevance of an LLM-generated answer to a given question. Your job is to analyze the answer and compare it to the provided ground truth phrases, then assign a relevance score between 0 and 5.
Please follow these guidelines:
Read the question, LLM-generated answer, and ground truth phrases carefully.
Evaluate how well the LLM-generated answer addresses the question and aligns with the ground truth phrases.
Assign a relevance score using the following scale:
0: Completely irrelevant or incorrect
1: Mostly irrelevant with minor relevant points
2: Partially relevant but missing key information
3: Moderately relevant with some alignment to ground truth
4: Highly relevant with most key points covered
5: Perfectly relevant and comprehensive
Please respond with a single integer between 0 and 5, which is your score. Do not add any text before the score no matter what.
Here is your input:
"""


def relevance(question: str, generated: str, ground_truth: str) -> float:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": relevance_prompt
            },
            {
                "role": "user",
                "content": "original question:" + question + "\n llm generated answer: " + generated + "\n ground truth" + ground_truth
            }
        ]
    )
    try:
        relevance = int(response.choices[0].message.content[0])
    except:
        print("error")
        relevance = -1
    return relevance / 5


groundedness_prompt = """
You are an AI assistant tasked with evaluating the groundedness of an LLM-generated answer to a given question. Your job is to analyze the answer and compare it to the provided retrieved context, then assign a groundedness score between 0 and 5.

Please follow these guidelines:

1. Read the question, LLM-generated answer, and retrieved context carefully.
2. Evaluate how well the LLM-generated answer is supported by the information in the retrieved context.
3. Assign a groundedness score using the following scale:
   0: Completely ungrounded or contradictory to the context
   1: Mostly ungrounded with minor supported points
   2: Partially grounded but with significant unsupported claims
   3: Moderately grounded with some unsupported information
   4: Highly grounded with most claims supported by the context
   5: Perfectly grounded and fully supported by the retrieved context

Please respond with a single integer between 0 and 5, which is your score. Do not add any text before the score no matter what.

Here is your input:
"""
def groundedness(question: str, generated: str, retrieved: list[str]) -> float:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": groundedness_prompt
            },
            {
                "role": "user",
                "content": "original question:" + question + "llm generated answer: " + generated + "\n   retrieved context: " + str(retrieved)
            }
        ]
    )
    try:
        groundedness = int(response.choices[0].message.content[0])
    except:
        print("error")
        groundedness = -1
    return groundedness / 5

rag_system = PDFRAGSystem(api_key=os.getenv("OPENAI_API_KEY"), search_endpoint=os.getenv("SEARCH_ENDPOINT"), search_api_key=os.getenv("SEARCH_API_KEY"), index_name=os.getenv("INDEX_NAME"))

data = []
with open('qa.tsv', 'r') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for line in tsv_reader:
        try:
            answer, question, ground_truth = line[0], line[1], line[2]
            data.append((question, answer, ground_truth))
        except:
            print("line is not list or line has less than 3 columns")

with open('output.json', 'w') as file:
    results = []
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    for line in tqdm.tqdm(data, desc="Processing lines"):
        question, answer, ground_truth = line
        response = rag_system.get_response(question)
        generated_answer = response["answer"]
        sources = response["sources"]
        result = {
            'question': question,
            'answer': answer,
            'ground_truth': ground_truth,
            'generated_answer': generated_answer,
            'retrieved sources': sources,
            'accuracy': accuracy(question, generated_answer, answer),
            'relevance': relevance(question, generated_answer, ground_truth),
            'groundedness': groundedness(question, generated_answer, sources)
        }
        results.append(result)
        json.dump(results, file)
    json.dump(results, file)
    sys.stdout.close()
    sys.stdout = original_stdout