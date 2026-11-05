from flask import Blueprint, request, jsonify
from database import Database
from sqlalchemy.exc import IntegrityError

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


@allenatore_bp.route("/allenatori", methods=["GET"])
def getAllenatori():
    db = Database() 
    risultato = db.get_allenatori()
    return jsonify(risultato), 200  

@allenatore_bp.route("/allenatori/<int:id>", methods=["GET"])
def getAllenatoreId(id):
    db = Database() 
    risultato = db.get_allenatore_id(id)
    if risultato is None:
        return jsonify({"errore": "Allenatore non trovato"}), 404
    return jsonify(risultato), 200        

@allenatore_bp.route("/allenatori/<int:id>", methods=["DELETE"])
def deleteAllenatore(id):
    db=Database()  
    try:
        risultato=db.deleteAllenatore(id)
        if risultato == 0:
            return "nessuna riga eliminata",404
        else:
            return "",204
    except IntegrityError:
        return "conflitto chiave esterna",409         