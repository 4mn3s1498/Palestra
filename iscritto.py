
from flask import Blueprint, request, jsonify
from database import Database

iscritto_bp = Blueprint("iscritto", __name__)


@iscritto_bp.route("/iscritti", methods=["POST"])
def creaIscritto():
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "JSON mancante o non valido"}), 400

    nome = dati.get("nome")
    cognome = dati.get("cognome")
    data = dati.get("dataNascita")

    if not nome or not cognome:
        return jsonify({"errore": "Nome e cognome obbligatori"}), 400

    db = Database()

    try:
        risultato = db.inserisci_iscritto(nome, cognome, data)
        return jsonify(risultato), 201
    except Exception:
        return jsonify({"errore": "Errore durante la creazione dell'iscritto"}), 500
