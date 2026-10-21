CREATE TABLE Iscritto (
    idIscritto SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    dataNascita DATE
);

CREATE TABLE Allenatore (
    idAllenatore SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    dataNascita DATE,
    compenso DECIMAL(8,2)
);

CREATE TABLE Abbonamento (
    idAbbonamento SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    dataScadenza DATE NOT NULL,
    idIscritto INT,
    FOREIGN KEY (idIscritto) REFERENCES Iscritto(idIscritto)
);

CREATE TABLE Scheda (
    idScheda SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    livello VARCHAR(50),
    idAllenatore INT,
    FOREIGN KEY (idAllenatore) REFERENCES Allenatore(idAllenatore)
);

CREATE TABLE Turno (
    idTurno SERIAL PRIMARY KEY,
    giorno VARCHAR(15),
    oraInizio TIME,
    oraFine TIME,
    idAllenatore INT,
    FOREIGN KEY (idAllenatore) REFERENCES Allenatore(idAllenatore)
);

CREATE TABLE Macchinario (
    idMacchinario SERIAL PRIMARY KEY,
    anno INT,
    dataUltimaManutenzione DATE NOT NULL,
    stato VARCHAR(30)
);

CREATE TABLE AssegnazioneScheda (
    idIscritto INT,
    idScheda INT,
    PRIMARY KEY (idIscritto, idScheda),
    FOREIGN KEY (idIscritto) REFERENCES Iscritto(idIscritto),
    FOREIGN KEY (idScheda) REFERENCES Scheda(idScheda)
);