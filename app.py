
from flask import Flask
from iscritti import iscritti_bp
from allenatori import allenatore_bp
from database import Database
from macchinari import macchinario_bp
from abbonamenti import abbonamento_bp
from turni import turno_bp
from schede import schede_bp
from assegnazioneSchede import assegnazioneSchede_bp
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.register_blueprint(iscritti_bp)
app.register_blueprint(allenatore_bp)
app.register_blueprint(macchinario_bp)
app.register_blueprint(abbonamento_bp)
app.register_blueprint(turno_bp)
app.register_blueprint(schede_bp)
app.register_blueprint(assegnazioneSchede_bp)

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
