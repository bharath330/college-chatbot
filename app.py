from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Open SQLite connection only once
conn = sqlite3.connect('college.db', check_same_thread=False)
cur = conn.cursor()

def get_answer(topic):
    cur.execute("SELECT answer FROM info WHERE topic=?", (topic,))
    row = cur.fetchone()
    return row[0] if row else "Sorry, I don't have that info."

@app.route('/')
def index():
    return "College Chatbot is running."

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName', '').lower()

    # Convert intent like 'ask_fee' to 'mtech_fee' manually or by mapping
    # This is an example - update as needed:
    intent_map = {
        'ask_fee': 'mtech_fee',
        'ask_hostel': 'hostel',
        'ask_btech_fee': 'btech_fee'
    }

    topic = intent_map.get(intent, intent)
    answer = get_answer(topic)

    return jsonify({'fulfillmentText': answer})

if __name__ == '__main__':
    app.run()
