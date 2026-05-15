-- app/db/init.sql
DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL
);

DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS matricula_sequence;

CREATE TABLE matricula_sequence (
    curso TEXT PRIMARY KEY,
    ultimo INTEGER NOT NULL DEFAULT 0
);
INSERT INTO matricula_sequence (curso) VALUES ('GES'), ('GEC');

CREATE TABLE alunos (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    matricula INTEGER NOT NULL,
    curso TEXT NOT NULL CHECK (curso IN ('GES', 'GEC'))
);