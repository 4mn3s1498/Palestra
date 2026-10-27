
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
