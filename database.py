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
