import openpyxl
import flask, jsonify
from metrics import Metrics
from RAG_Core import PDFRAGSystem

app = flask.Flask(__name__)
metrics = Metrics()
rag = PDFRAGSystem()

workbook = openpyxl.load_workbook("back-end\evaluation\Dataset.xlsx")
sheet = workbook.active

@app.route("/")
def home():
    return "System Start"

@app.route("/calculate_metrics", methods=["GET"])
def calculate_metrics():
    for row in sheet.iter_rows(min_row=3,max_col=4, max_row=50, values_only=True):
        metrics.eval_row(
            question=row[1],
            generated_answer= rag.get_response(row[1]),
            correct_answer=row[0],
            ground_truth=row[2].split(','),#dont appear to be split
            relevant_docs=row[3].split(','),
            retrieved_chunks=[],#don't kno what to put here
            retrieved_docs=[],#same with chunks?
        )
    return jsonify(metrics.results)

@app.route("/macro_metrics", methods=["GET"])
def get_macro_metrics():
    return jsonify(metrics.macro_metrics())

if __name__ == '__main__':
    try:
        print("Running metrics app...")
        calculate_metrics()
        get_macro_metrics()
        print("Metrics complete!")
    except Exception as e:
        print(f"Error running metrics: {str(e)}")
    app.run(debug=True)