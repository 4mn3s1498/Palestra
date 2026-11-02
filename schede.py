from flask import Blueprint, request, jsonify
from database import Database

schede_bp = Blueprint("scheda", __name__)

@schede_bp.route("/schede", methods=["POST"])
def scheda():
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "JSON mancante o non valido"}), 400

    nome = dati.get("nome")
    livello = dati.get("livello")
    idAllenatore = dati.get("idAllenatore")

    if not nome or not idAllenatore:
        return jsonify({
            "errore": "Nome e ID allenatore sono obbligatori"
        }), 400

    db = Database()

    try:
        risultato = db.inserisci_scheda(
            nome, livello, idAllenatore
        )
        return jsonify(risultato), 201

    except ValueError as errore:
        return jsonify({"errore": str(errore)}), 404

    except Exception as errore:
        print(errore)
        return jsonify({
            "errore": "Errore durante la creazione della scheda"
        }), 500

@schede_bp.route("/schede", methods=["GET"])
def getSchede():
    db = Database() 
    risultato = db.get_schede()
    return jsonify(risultato), 200  

@schede_bp.route("/schede/<int:id>", methods=["GET"])
def getSchedeId(id):
    db = Database() 
    risultato = db.get_schede_id(id)
    if risultato is None:
        return jsonify({"errore": "Scheda non trovata"}), 404
    return jsonify(risultato), 200   