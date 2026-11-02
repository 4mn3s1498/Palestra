from flask import Blueprint, request, jsonify
from database import Database

assegnazioneSchede_bp = Blueprint("assegnazioneScheda", __name__)

@assegnazioneSchede_bp.route("/assegnazioneSchede", methods=["POST"])
def assegnazioneScheda():
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "JSON mancante o non valido"}), 400

    idScheda=dati.get("idScheda")
    idIscritto=dati.get("idIscritto")   
    
    if not idScheda or not idIscritto:
        return jsonify({
            "errore": "Id Scheda e Id Iscritto sono obbligatori"
        }), 400

    db = Database()

    try:
        risultato = db.inserisci_assegnazioneScheda(
            idScheda, idIscritto
        )
        return jsonify(risultato), 201

    except ValueError as errore:
        return jsonify({"errore": str(errore)}), 404

    except Exception as errore:
        print(errore)
        return jsonify({
            "errore": "Errore durante l'assegnazione della scheda"
        }), 500

@assegnazioneSchede_bp.route("/assegnazioneSchede", methods=["GET"])
def getAssegnazioneSchede():
    db = Database() 
    risultato = db.get_assegnazioneSchede()
    return jsonify(risultato), 200  

@assegnazioneSchede_bp.route("/assegnazioneSchede/<int:idScheda>/<int:idIscritto>", methods=["GET"])
def getAssegnazioneSchedeId(idScheda, idIscritto):
    db = Database()
    risultato = db.get_assegnazione_schede_id(idScheda, idIscritto)

    if risultato is None:
        return jsonify({"errore": "Assegnazione Scheda non trovata"}), 404

    return jsonify(risultato), 200