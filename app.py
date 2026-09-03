from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'mydatabase')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'flask_tutorial')

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    print('Connected to MongoDB')
except ConnectionFailure as error:
    client = None
    collection = None
    print(f'Failed to connect to MongoDB: {error}')

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.now().strftime('%A %d/%m/%Y')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/time')
def time():
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('time.html', current_time=current_time)

@app.route('/submit', methods=['POST'])
def submit():
    if collection is None:
        return 'MongoDB connection is not available.', 500

    form_data = dict(request.form)
    if not form_data:
        return 'No data submitted.', 400

    form_data['submitted_at'] = datetime.utcnow()

    try:
        collection.insert_one(form_data)
    except PyMongoError as error:
        return f'Error saving to MongoDB: {error}', 500

    return redirect(url_for('view'))

@app.route('/view')
def view():
    if collection is None:
        return 'MongoDB connection is not available.', 500

    items = list(collection.find().sort('_id', -1))
    return render_template('view.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
 