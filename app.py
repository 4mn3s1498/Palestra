
from flask import Flask
from iscritto import iscritto_bp
from allenatore import allenatore_bp
from database import Database

app = Flask(__name__)
app.register_blueprint(iscritto_bp)
app.register_blueprint(allenatore_bp)

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
