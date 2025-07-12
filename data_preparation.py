import mysql.connector
from db_config import db_config
conn = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"]
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot")
cursor.execute("USE chatbot")
cursor.execute("""
CREATE TABLE IF NOT EXISTS qa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255),
    answer VARCHAR(255)
)
""")

qa_pairs = [
    ("hello", "Hi!"),
    ("how are you", "I am good, thank you!"),
    ("what is your name", "I am a chatbot."),
    ("bye", "Goodbye!"),
    ("who created you", "I was developed by Hardik."),
    ("what is your age", "I know mine it is 18.")
]

cursor.executemany(
    "INSERT IGNORE INTO qa (question, answer) VALUES (%s, %s)", qa_pairs)

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_number INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    class VARCHAR(20),
    section VARCHAR(5)
)
""")

students_data = [
    (101, "Rahul", "Sharma", "10", "A"),
    (102, "Anjali", "Verma", "10", "B"),
    (103, "Aman", "Gupta", "11", "A")
]

cursor.executemany("""
INSERT IGNORE INTO students 
(roll_number, first_name, last_name, class, section) 
VALUES (%s, %s, %s, %s, %s)
""", students_data)

conn.commit()
cursor.close()
conn.close()