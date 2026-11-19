
# Gestionale Palestra

Progetto backend per la gestione di una palestra, sviluppato con Python, Flask, SQLAlchemy e PostgreSQL.

## Tecnologie utilizzate

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Docker
- Git e GitHub

## Funzionalità

Il progetto permette di gestire:

- Iscritti
- Allenatori
- Macchinari
- Abbonamenti
- Turni
- Schede di allenamento
- Assegnazioni delle schede agli iscritti

## API REST

Il backend espone endpoint REST per consultare e gestire i dati del gestionale.

Esempi:

- `GET /iscritti`
- `GET /iscritti/<id>`
- `GET /iscritti/<id>/abbonamenti`
- `GET /allenatori/<id>/turni`

## Database

Il database utilizzato è PostgreSQL, eseguito tramite Docker.

## Obiettivo

Realizzare un gestionale completo per una palestra, approfondendo lo sviluppo backend, le API REST, le query SQL e l'interazione con database relazionali.
