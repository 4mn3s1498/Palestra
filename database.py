from sqlalchemy import create_engine, text

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

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            print("connessione riuscita")
            return True

        except Exception as errore:
            print(f"Errore di connessione: {errore}")
            return False

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
