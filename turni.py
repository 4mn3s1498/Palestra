from flask import Blueprint, request, jsonify
from database import Database
from sqlalchemy.exc import IntegrityError

turno_bp = Blueprint("turno", __name__)

@turno_bp.route("/turni", methods=["POST"])
def turno():
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "JSON mancante o non valido"}), 400

    giorno = dati.get("giorno")
    oraInizio = dati.get("oraInizio")
    oraFine = dati.get("oraFine")
    idAllenatore = dati.get("idAllenatore")

    if not giorno or not oraInizio or not oraFine or not idAllenatore:
        return jsonify({
            "errore": "Giorno, orari e ID allenatore sono obbligatori"
        }), 400

    db = Database()

    try:
        risultato = db.inserisci_turno(
            giorno, oraInizio, oraFine, idAllenatore
        )
        return jsonify(risultato), 201

    except ValueError as errore:
        return jsonify({"errore": str(errore)}), 404

    except Exception as errore:
        print(errore)
        return jsonify({
            "errore": "Errore durante la creazione del turno"
        }), 500

@turno_bp.route("/turni", methods=["GET"])
def getTurni():
    db = Database() 
    risultato = db.get_turni()
    return jsonify(risultato), 200  

@turno_bp.route("/turni/<int:id>", methods=["GET"])
def getTurnoId(id):
    db = Database() 
    risultato = db.get_turno_id(id)
    if risultato is None:
        return jsonify({"errore": "Turno non trovato"}), 404
    return jsonify(risultato), 200   

@turno_bp.route("/turni/<int:id>", methods=["DELETE"]) 
def deleteTurno(id):
    db=Database()
    risultato=db.deleteTurno(id)
    if risultato == 0:
        return "Nessuna riga eliminata", 404
    else:
        return "", 204 

@turno_bp.route("/turni/<int:id>", methods=["PUT"])
def updateTurno(id):
    dati = request.get_json()
    if dati is None:
        return "Nessun dato ricevuto", 400
    db = Database()
    try:
        risultato = db.updateTurno(id, dati)
        if risultato is None:
            return "Nessuna riga modificata", 404
        else:
            dto = {
                "idTurno": id,
                "giorno": risultato._mapping["giorno"],
                "oraInizio":risultato._mapping["orainizio"].isoformat(),
                "oraFine":risultato._mapping["orafine"].isoformat(),
                "idAllenatore": risultato._mapping["idallenatore"],
              
            }
            return jsonify(dto), 200
    except IntegrityError:
        return "Conflitto chiave esterna", 409    

           