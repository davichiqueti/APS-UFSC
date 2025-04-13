# APS-UFSC

Este projeto é uma aplicação em Python desktop para a máteria de Análise e Projeto de Sistemas (APS) do curso de sistemas de informação da UFSC.

## Tópicos

- [Iniciando aplicação](#iniciando-aplicação)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Setup](#setup)
    - [Pré requisitos](#pré-requisitos)
    - [Instalação](#instalação)

## Iniciando aplicação

Todos os arquivos e módulos são escritos usando como diretório base a pasta `src` (Abreviação "source code"). Por isso, para executar o projeto, primeiramente acesse o diretorio com:

```bash
cd src/
```

Então, execute o arquivo main.py para iniciar a aplicação:
```bash
python main.py
```

## Estrutura do projeto

```
APS-UFSC/
├── src/
│   ├── controllers/       # Lógica da aplicação e gerenciamento de usuários
│   ├── database/          # Gerenciamento da conexão e configuração do banco de dados
│   │   ├── migrations/    # Scripts SQL para criação e atualização das tabelas e estruturas do banco
│   ├── models/            # Modelos de dados e validação
│   ├── repositories/      # Camada de acesso aos dados no banco de dados
│   ├── views/             # Interfaces de usuário
│   ├── .env.example       # Exemplo de variáveis de ambiente
│   ├── main.py            # Ponto de entrada da aplicação
├── tests/                 # Testes automatizados da aplicação
├── .gitignore             # Regras para ignorar arquivos no Git
├── pytest.ini             # Configuração do Pytest
└── README.md              # Documentação do projeto
```

## Setup

### Pré requisitos

- Python 3.11

### Instalação

1. Criar o arquivo `.env` com base no arquivo `.env.example`:

2. Criar ambiente virtual (Opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instalação de dependências:
```bash
pip install -r requirements.txt
```
