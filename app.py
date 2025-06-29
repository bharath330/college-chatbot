from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_answer(topic):
    conn=sqlite3.connect('college.db')
    cur=conn.cursor()
    cur.execute("SELECT answer FROM info WHERE topic=?", (topic,))
    row=cur.fetchone()
    conn.close()
    return row[0] if row else "Sorry, I don't have that info."

@app.route('/')
def index():
    return "College Chatbot is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    req=request.get_json()
    intent=req['queryResult']['intent']['displayName']
    answer=get_answer(intent.lower())
    return jsonify({'fulfillmentText': answer})

if __name__ == '__main__':
    app.run()
