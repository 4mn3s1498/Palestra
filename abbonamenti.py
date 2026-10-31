from flask import Blueprint, request, jsonify
from database import Database

abbonamento_bp = Blueprint("abbonamento", __name__)

@abbonamento_bp.route("/abbonamenti", methods=["POST"])
def abbonamento():
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "JSON mancante o non valido"}), 400

    tipo = dati.get("tipo")
    dataScadenza = dati.get("dataScadenza")
    idIscritto = dati.get("idIscritto")

    if not tipo or not dataScadenza or not idIscritto:
        return jsonify({"errore": "Tipo, data di scadenza e ID iscritto sono obbligatori"}), 400

    db = Database()

 
    try:
        risultato = db.inserisci_abbonamento(tipo, dataScadenza, idIscritto)
        return jsonify(risultato), 201

    except ValueError as errore:
        return jsonify({"errore": str(errore)}), 404

    except Exception as errore:
        print(errore)
        return jsonify({"errore": "Errore durante la creazione dell'abbonamento"}), 500

@abbonamento_bp.route("/abbonamenti", methods=["GET"])
def getAbbonamenti():
    db = Database() 
    risultato = db.get_abbonamenti()
    return jsonify(risultato), 200  

@abbonamento_bp.route("/abbonamenti/<int:id>", methods=["GET"])
def getAbbonamentoId(id):
    db = Database() 
    risultato = db.get_abbonamento_id(id)
    if risultato is None:
        return jsonify({"errore": "Abbonamento non trovato"}), 404
    return jsonify(risultato), 200                
