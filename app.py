
from flask import Flask
from database import Database

app = Flask(__name__)

@app.route("/")
def saluta():
    return "Hello World!"

@app.route("/test-connession")
def test_connession():
    db = Database()
    if db.test_connection():
        return "connessione riuscita", 200
    return "connessione fallita", 500

if __name__ == "__main__":
    app.run(debug=True)
