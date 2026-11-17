
from flask import Blueprint, request, jsonify
from database import Database
from sqlalchemy.exc import IntegrityError

macchinario_bp = Blueprint("macchinario", __name__)

@macchinario_bp.route("/macchinario", methods=["POST"])
def creaMacchinario():
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "JSON mancante o non valido"}), 400

    anno = dati.get("anno")
    dataManutenzione = dati.get("dataManutenzione")
    stato = dati.get("stato")

    if not dataManutenzione:
        return jsonify({"errore": "Data utltima manutenzione necessaria"}), 400

    db = Database()

    try:
        risultato = db.inserisci_macchinario(anno, dataManutenzione, stato)
        return jsonify(risultato), 201
    except Exception as errore:
        print(errore)
        return jsonify({"errore": "Errore durante la creazione del macchinario"}), 500

@macchinario_bp.route("/macchinario", methods=["GET"])
def getMacchinari():
    db = Database() 
    risultato = db.get_macchinari()
    return jsonify(risultato), 200  

@macchinario_bp.route("/macchinario/<int:id>", methods=["GET"])
def getMacchinarioId(id):
    db = Database() 
    risultato = db.get_macchinario_id(id)
    if risultato is None:
        return jsonify({"errore": "Macchinario non trovato"}), 404
    return jsonify(risultato), 200        

@macchinario_bp.route("/macchinario/<int:id>", methods=["DELETE"])
def deleteMacchinario(id):
    db=Database()
    risultato=db.deleteMacchinario(id) 
    if risultato == 0:
        return "Nessuna riga eliminata",404
    else:
        return "",204      

@macchinario_bp.route("/macchinario/<int:id>", methods=["PUT"])
def updateMacchinario(id):
    dati = request.get_json()

    if dati is None:
        return "Nessun dato ricevuto", 400

    db = Database()

    try:
        risultato = db.updateMacchinario(id, dati)

        if risultato is None:
            return "Nessuna riga modificata", 404

        else:
            dto = {
                "idMacchinario": id,
                "anno": risultato._mapping["anno"],
                "dataManutenzione":risultato._mapping["dataultimamanutenzione"],
                "stato": risultato._mapping["stato"],
                
            }

            return jsonify(dto), 200

    except IntegrityError:
        return "Conflitto chiave esterna", 409        