from flask import Flask, request
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = pymongo.MongoClient(MONGO_URI)

db = client._test

collection = db['flask_tutorial']

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():

    form_data = dict(request.form)
    
    collection.insert_one(form_data)

    return 'Data submitted successfully!'



@app.route('/view')
def view():

    data =  collection.find()

    data = list(data)

    for item in data:

        print(item)

        del item['_id']

        data = {
            'data': data

        }

        return data
    

if __name__ == '__main__':
    app.run(debug=True)
 