print("Starting Flask server...")
from flask import Flask, render_template, request, jsonify
import chatbot 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')

    doc = chatbot.nlp(question.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]

    roll_number = None
    for token in tokens:
        if token.isdigit():
            roll_number = int(token)
            break

    if roll_number:
        response = chatbot.get_multiple_student_info(roll_number, question)
    else:
        response = chatbot.get_answer(question)
        if response == "Out of bound!":
            response = "Sorry, I don't understand the question."

    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True,port = 5050)