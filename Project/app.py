from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://dummy:1234@cluster.mongodb.net/mydatabase?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["mydatabase"]
collection = db["users"]

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"]
        }

        collection.insert_one(data)

        return redirect(url_for("success"))

    except Exception as e:
        return render_template(
            "form.html",
            error=f"Error: {str(e)}"
        )

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)