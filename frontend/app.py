from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.now().strftime('%A %d/%m/%Y')

    current_time = datetime.now().strftime('%H:%M:%S')

    return f"Today is {day_of_week} and the current time is {current_time}."
    

if __name__ == '__main__':
    app.run(debug=True)
 