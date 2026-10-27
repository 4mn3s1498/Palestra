from flask import Blueprint, request, jsonify
from database import Database

allenatore_bp = Blueprint("allenatore", __name__)

@allenatore_bp.route("/allenatore", methods=["POST"])
def creaAllenatore():
    dati = request.get_json()
    nome = dati.get("nome")
    cognome = dati.get("cognome")
    data = dati.get("dataNascita")
    compenso = dati.get("compenso")

    if not nome or not cognome:
        return jsonify({"errore": "Dati mancanti"}), 400
    
    db=Database()
    
    try:
        risultato = db.inserisci_allenatore(nome, cognome, data, compenso)
        return jsonify(risultato), 201
    except Exception as errore:
        print(errore)
        return jsonify({"errore": "Errore durante la creazione dell'allenatore"}), 500