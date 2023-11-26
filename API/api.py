from flask import Flask, request, jsonify
from llm import LanguageModel

app = Flask(__name__)
llm = LanguageModel()

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.json
    query = data['query']
    answer = llm.generate_contextual_answer(query)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
