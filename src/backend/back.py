"""
A sample backend server. Saves and retrieves entries using mongodb
"""
import os
import time
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import bleach

# Configuration
DEFAULT_GUESTBOOK_DB_ADDR = "127.0.0.1:27017"
GUESTBOOK_DB_ADDR = os.environ.get('GUESTBOOK_DB_ADDR', DEFAULT_GUESTBOOK_DB_ADDR)
DEFAULT_PORT = 8321
PORT = os.environ.get('PORT', DEFAULT_PORT)
DEFAULT_HOST = "127.0.0.1"
HOST = os.environ.get('HOST', DEFAULT_HOST)

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = f'mongodb://{GUESTBOOK_DB_ADDR}/guestbook'
mongo = PyMongo(app)

# Define helper functions
def clean_message(message):
    """Sanitizes the message content using bleach.clean to prevent XSS attacks."""
    return bleach.clean(message)

def create_message_data(author, message):
    """Creates a dictionary with the author, message, and timestamp."""
    return {'author': clean_message(author),
            'message': clean_message(message),
            'date': time.time()}

# Define routes
@app.route('/messages', methods=['GET'])
def get_messages():
    """Retrieves and returns a list of messages from the database."""
    field_mask = {'author':1, 'message':1, 'date':1, '_id':0}
    msg_list = list(mongo.db.messages.find({}, field_mask).sort("_id", -1))
    return jsonify(msg_list), 201

@app.route('/messages', methods=['POST'])
def add_message():
    """Saves a new message to the database."""
    raw_data = request.get_json()
    msg_data = create_message_data(raw_data['author'], raw_data['message'])
    mongo.db.messages.insert_one(msg_data)
    return jsonify({}), 201

# Main execution
if __name__ == '__main__':
    # Start Flask server
    # Flask's debug mode is unrelated to ptvsd debugger used by Cloud Code
    app.run(debug=False, port=PORT, host=HOST)
