
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
