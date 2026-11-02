from sqlalchemy import create_engine, text
# crea database 
class Database:
    def __init__(self):
        self.database = "amnesia"
        self.host = "localhost"
        self.username = "amnesia"
        self.password = "password1234"
        self.port = 5432

        self.engine = create_engine(
            f"postgresql+psycopg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
# crea connessione
    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            print("connessione riuscita")
            return True

        except Exception as errore:
            print(f"Errore di connessione: {errore}")
            return False
#iscritto
    def inserisci_iscritto(self, nome, cognome, data):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    INSERT INTO iscritto (nome, cognome, datanascita)
                    VALUES (:nome, :cognome, :data)
                    RETURNING idiscritto
                """),
                {
                    "nome": nome,
                    "cognome": cognome,
                    "data": data
                }
            )

            id_iscritto = risultato.scalar_one()

        return {
            "idIscritto": id_iscritto,
            "nome": nome,
            "cognome": cognome,
            "dataNascita": data
        }
        #allenatore
    def inserisci_allenatore(self, nome, cognome, data, compenso):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    INSERT INTO allenatore (nome, cognome, datanascita, compenso)
                    VALUES (:nome, :cognome, :data, :compenso)
                    RETURNING idallenatore
                """),
                {
                    "nome": nome,
                    "cognome": cognome,
                    "data": data,
                    "compenso": compenso
                }
            )

            id_allenatore = risultato.scalar_one()

        return {
            "id_allenatore": id_allenatore,
            "nome": nome,
            "cognome": cognome,
            "dataNascita": data,
            "compenso": compenso
        }
#macchinari    
       
    def inserisci_macchinario(self, anno, dataManutenzione, stato):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    INSERT INTO Macchinario (anno, dataUltimaManutenzione, stato)
                    VALUES (:anno, :dataManutenzione, :stato)
                    RETURNING idMacchinario
                """),
                {
                    "anno": anno,
                    "dataManutenzione": dataManutenzione,
                    "stato": stato
                }
            )

            id_macchinario = risultato.scalar_one()

        return {
            "idMacchinario": id_macchinario,
            "anno": anno,
            "dataUltimaManutenzione": dataManutenzione,
            "stato": stato
        }
     #abbonamenti 
  
    def inserisci_abbonamento(self, tipo, dataScadenza, idIscritto):
        with self.engine.begin() as conn:

            # Controlla se l'iscritto esiste
            iscritto = conn.execute(
                text("""
                    SELECT idIscritto
                    FROM Iscritto
                    WHERE idIscritto = :idIscritto
                """),
                {"idIscritto": idIscritto}
            )

            iscritto = iscritto.fetchone()

            if iscritto is None:
                raise ValueError("Iscritto non trovato")

            # Inserisce l'abbonamento
            risultato = conn.execute(
                text("""
                    INSERT INTO Abbonamento (tipo, dataScadenza, idIscritto)
                    VALUES (:tipo, :dataScadenza, :idIscritto)
                    RETURNING idAbbonamento
                """),
                {
                    "tipo": tipo,
                    "dataScadenza": dataScadenza,
                    "idIscritto": idIscritto
                }
            )

            id_abbonamento = risultato.scalar_one()

        return {
            "idAbbonamento": id_abbonamento,
            "tipo": tipo,
            "dataScadenza": dataScadenza,
            "idIscritto": idIscritto
        }
        #turni
 
    def inserisci_turno(self, giorno, oraInizio, oraFine, idAllenatore):
        with self.engine.begin() as conn:

            # Controlla se l'allenatore esiste
            risultato_controllo = conn.execute(
                text("""
                    SELECT idAllenatore
                    FROM Allenatore
                    WHERE idAllenatore = :idAllenatore
                """),
                {"idAllenatore": idAllenatore}
            )

            allenatore = risultato_controllo.fetchone()

            if allenatore is None:
                raise ValueError("Allenatore non trovato")

            # Inserisce il turno
            risultato = conn.execute(
                text("""
                    INSERT INTO Turno (giorno, oraInizio, oraFine, idAllenatore)
                    VALUES (:giorno, :oraInizio, :oraFine, :idAllenatore)
                    RETURNING idTurno
                """),
                {
                    "giorno": giorno,
                    "oraInizio": oraInizio,
                    "oraFine": oraFine,
                    "idAllenatore": idAllenatore
                }
            )

            id_turno = risultato.scalar_one()

        return {
            "idTurno": id_turno,
            "giorno": giorno,
            "oraInizio": oraInizio,
            "oraFine": oraFine,
            "idAllenatore": idAllenatore
        }
        #schede

    def inserisci_scheda(self, nome, livello, idAllenatore):
        with self.engine.begin() as conn:

        
            allenatore = conn.execute(
                text("""
                    SELECT idAllenatore
                    FROM Allenatore
                    WHERE idAllenatore = :idAllenatore
                """),
                {"idAllenatore": idAllenatore}
            )

            allenatore = allenatore.fetchone()

            if allenatore is None:
                raise ValueError("Allenatore non trovato")

            
            risultato = conn.execute(
                text("""
                    INSERT INTO Scheda (nome, livello, idAllenatore)
                    VALUES (:nome, :livello, :idAllenatore)
                    RETURNING idScheda
                """),
                {
                    "nome": nome,
                    "livello": livello,
                    "idAllenatore": idAllenatore
                }
            )

            id_scheda = risultato.scalar_one()

        return {
            "idScheda": id_scheda,
            "nome": nome,
            "livello": livello,
            "idAllenatore": idAllenatore
        }
        #assScheda

    def inserisci_assegnazioneScheda(self, idScheda, idIscritto):
        with self.engine.begin() as conn:
            risultato_scheda = conn.execute(
                text("""
                    SELECT idScheda
                    FROM Scheda
                    WHERE idScheda = :idScheda
                """),
                {"idScheda": idScheda}
            )

            scheda_trovata = risultato_scheda.fetchone()

            if scheda_trovata is None:
                raise ValueError("Scheda non trovata")

            risultato_iscritto = conn.execute(
                text("""
                    SELECT idIscritto
                    FROM Iscritto
                    WHERE idIscritto = :idIscritto
                """),
                {"idIscritto": idIscritto}
            )

            iscritto_trovato = risultato_iscritto.fetchone()

            if iscritto_trovato is None:
                raise ValueError("Iscritto non trovato")

            conn.execute(
                text("""
                    INSERT INTO AssegnazioneScheda (idScheda, idIscritto)
                    VALUES (:idScheda, :idIscritto)
                """),
                {
                    "idScheda": idScheda,
                    "idIscritto": idIscritto
                }
            )

        return {
            "idScheda": idScheda,
            "idIscritto": idIscritto
        }
#GET GET GET 
    def get_iscritti(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM iscritto
                """)
            )

            iscritti = risultato.fetchall()
            dto = []

            for iscritto in iscritti:
                dto.append({
                    "idIscritto": iscritto[0],
                    "nome": iscritto[1],
                    "cognome": iscritto[2],
                    "dataNascita": iscritto[3]
                })

        return dto

    def get_iscrittoId(self, id):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM iscritto
                    WHERE idiscritto = :id
                """),
                {"id": id}
            )

            iscritto = risultato.fetchone()

            if iscritto is None:
                return None

            return {
                "idIscritto": iscritto[0],
                "nome": iscritto[1],
                "cognome": iscritto[2],
                "dataNascita": iscritto[3]
            }

    def get_allenatori(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM allenatore
                """)
            )

            allenatori = risultato.fetchall()
            dto = []

            for allenatore in allenatori:
                dto.append({
                    "idAllenatore": allenatore[0],
                    "nome": allenatore[1],
                    "cognome": allenatore[2],
                    "dataNascita": allenatore[3],
                    "compenso": allenatore[4]
                })

        return dto
    def get_allenatore_id(self, id):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM allenatore
                    WHERE idAllenatore = :id
                """),
                {"id": id}
            )

            allenatore = risultato.fetchone()

            if allenatore is None:
                return None

            return {
                "idAllenatore": allenatore[0],
                "nome": allenatore[1],
                "cognome": allenatore[2],
                "dataNascita": allenatore[3],
                "compenso": allenatore[4]
            }

    def get_macchinari(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM macchinario
                """)
            )

            macchinari = risultato.fetchall()
            dto = []

            for macchinario in macchinari:
                dto.append({
                    "idMacchinario": macchinario[0],
                    "anno": macchinario[1],
                    "dataManutenzione": macchinario[2],
                    "stato": macchinario[3]
                })

            return dto

    def get_macchinario_id(self, id):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM macchinario
                    WHERE idMacchinario = :id
                """),
                {"id": id}
            )

            macchinario = risultato.fetchone()

            if macchinario is None:
                return None

            return {
                "idMacchinario": macchinario[0],
                "anno": macchinario[1],
                "dataManutenzione": macchinario[2],
                "stato": macchinario[3]
            }

    def get_abbonamenti(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM abbonamento
                """)
            )

            abbonamenti = risultato.fetchall()
            dto = []

            for abbonamento in abbonamenti:
                dto.append({
                    "idAbbonamenti": abbonamento[0],
                    "tipo": abbonamento[1],
                    "dataScadenza": abbonamento[2],
                    "idIscritto": abbonamento[3]
                })

            return dto

    def get_abbonamento_id(self, id):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM abbonamento
                    WHERE idAbbonamento = :id
                """),
                {"id": id}
            )

            abbonamento = risultato.fetchone()

            if abbonamento is None:
                return None

            return {
                "idAbbonamenti": abbonamento[0],
                "tipo": abbonamento[1],
                "dataScadenza": abbonamento[2],
                "idIscritto": abbonamento[3]
            }
     #turni       
    def get_turni(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM turno
                """)
            )

            turni = risultato.fetchall()
            dto = []

            for turno in turni:
                dto.append({
                    "idTurno": turno[0],
                    "giorno": turno[1],
                    "oraInizio": turno[2].isoformat(),
                    "oraFine": turno[3].isoformat(),
                    "idAllenatore": turno[4]
                })

            return dto

    def get_turno_id(self, id):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM turno
                    WHERE idTurno = :id
                """),
                {"id": id}
            )

            turno= risultato.fetchone()

            if turno is None:
                return None

            return {
                "idTurno": turno[0],
                "giorno": turno[1],
                "oraInizio": turno[2].isoformat(), 
                "oraFine": turno[3].isoformat(), 
                "idAllenatore": turno[4]
            }
    def get_schede(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM scheda
                """)
            )

            schede = risultato.fetchall()
            dto = []

            for scheda in schede:
                dto.append({
                    "idScheda":scheda[0],
                    "nome" : scheda[1],
                    "livello" : scheda[2],
                    "idAllenatore" : scheda[3]
                })

            return dto

    def get_schede_id(self, id):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM scheda
                    WHERE idScheda = :id
                """),
                {"id": id}
            )

            scheda= risultato.fetchone()

            if scheda is None:
                return None

            return {
                "idScheda":scheda[0],
                "nome" : scheda[1],
                "livello" : scheda[2],
                "idAllenatore" : scheda[3]
            }
     
    # assegnazioneSchede
    def get_assegnazioneSchede(self):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM AssegnazioneScheda
                """)
            )

            assegnazioni = risultato.fetchall()
            dto = []

            for assegnazione in assegnazioni:
                dto.append({
                    "idScheda": assegnazione[0],
                    "idIscritto": assegnazione[1]
                })

            return dto

    def get_assegnazione_schede_id(self, idScheda, idIscritto):
        with self.engine.begin() as conn:
            risultato = conn.execute(
                text("""
                    SELECT *
                    FROM AssegnazioneScheda
                    WHERE idScheda = :idScheda
                    AND idIscritto = :idIscritto
                """),
                {
                    "idScheda": idScheda,
                    "idIscritto": idIscritto
                }
            )

            assegnazione = risultato.fetchone()

            if assegnazione is None:
                return None

            return {
                "idScheda": assegnazione[0],
                "idIscritto": assegnazione[1]
            }
