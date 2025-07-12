import mysql.connector
from db_config import db_config
import os
import spacy

nlp = spacy.load("en_core_web_sm")

# Run data preparation script
os.system("python3 data_preparation.py")

# Connect to database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(buffered=True)

def get_answer(user_input):
    doc = nlp(user_input.lower())
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    cursor.execute("SELECT question, answer FROM qa")
    results = cursor.fetchall()
    for word in keywords:
        for q, a in results:
            if word in q.lower():
                return a
    return "Out of bound!"

def get_student_details(roll_input):
    try:
        roll_number = int(roll_input)
        cursor.execute("SELECT first_name, last_name, class, section FROM students WHERE roll_number = %s", (roll_number,))
        result = cursor.fetchone()
        if result:
            return f"Name: {result[0]} {result[1]}, Class: {result[2]}, Section: {result[3]}"
        else:
            return "Student not found!"
    except ValueError:
        return None

def get_multiple_student_info(roll_number, query):
    try:
        roll_number = int(roll_number)
        cursor.execute("SELECT first_name, last_name, class, section FROM students WHERE roll_number = %s", (roll_number,))
        result = cursor.fetchone()
        if not result:
            return "Student not found."
        doc = nlp(query.lower())
        tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
        keywords = " ".join(tokens)
        responses = []
        if ("first" in tokens and "name" in tokens) or "firstname" in keywords:
            responses.append(f"First Name: {result[0]}")
        if ("last" in tokens and "name" in tokens) or "lastname" in keywords:
            responses.append(f"Last Name: {result[1]}")
        if "class" in tokens:
            responses.append(f"Class: {result[2]}")
        if "section" in tokens:
            responses.append(f"Section: {result[3]}")
        if not responses:
            return f"Name: {result[0]} {result[1]}, Class: {result[2]}, Section: {result[3]}"
        return "\n".join(responses)
    except ValueError:
        return "Invalid roll number."

if __name__ == "__main__":
    print("Chatbot: Hello!")
    print("Chatbot: You can ask a question or enter a roll number.")
    print("Chatbot: Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Chatbot: Bye!")
            break

        doc = nlp(user_input.lower())
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]

        roll_number = None
        for token in tokens:
            if token.isdigit():
                roll_number = int(token)
                break

        if roll_number:
            response = get_multiple_student_info(roll_number, user_input)
            print("Chatbot:", response)
            continue

        student_info = get_student_details(user_input)
        if student_info:
            print("Chatbot:", student_info)
            continue

        response = get_answer(user_input)
        if response == "Out of bound!":
            print("Chatbot: Out of bound! Please enter a valid question or roll number.")
        else:
            print("Chatbot:", response)

    cursor.close()
    conn.close()