CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    username VARCHAR(60) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    birthdate DATE NOT NULL,
    encrypted_password TEXT NOT NULL
);
