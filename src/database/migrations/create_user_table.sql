CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    nome VARCHAR(60) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    foto TEXT,
    data_nascimento DATE NOT NULL,
    senha_criptografada TEXT NOT NULL
);
