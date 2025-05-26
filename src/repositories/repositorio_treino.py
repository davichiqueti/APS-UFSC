# repositories/repositorio_treino.py

from repositories.repositorio_base import RepositorioBase
from models.treino import Treino
from sqlalchemy.sql import text
import sqlalchemy
from datetime import date

from models.usuario import Usuario

class RepositorioTreino(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def criar(self, treino: Treino) -> None:
        query = text("""
        INSERT INTO treinos (descricao, foto, usuario, curtidas, "data")
        VALUES (:descricao, :foto, :usuario, :curtidas, :data)
        """)
        with self._conn.begin():
            self._conn.execute(
                statement = query,
                parameters = {
                    "descricao": treino.descricao,
                    "foto": treino.imagem,                          # no model é 'imagem'
                    "usuario": treino.usuario.id if treino.usuario else None,
                    "curtidas": treino.curtidas,
                    "data": treino.data.isoformat() if treino.data else None
                }
            )


    def buscar_por_usuario_id(self, usuario_id_autor: int) -> list[Treino]:
        """
        Busca todos os treinos registrados por um usuário específico (autor do treino).
        Retorna uma lista de objetos Treino.
        """
        treinos_encontrados = []
        # Query para buscar treinos e dados do usuário autor.
        # Ajuste os nomes das tabelas/colunas conforme seu banco.
        # Assumindo que 'treinos.usuario' armazena o ID do autor.
        # Assumindo que 'treinos.foto' armazena o caminho da imagem.
        # Assumindo que 'treinos' possui uma coluna 'duracao'.
        query = text("""
            SELECT 
                t.id as treino_id, t.descricao, t.duracao, t.foto as treino_imagem, 
                t.data as treino_data, t.curtidas as treino_curtidas,
                u.id as autor_id, u.cpf as autor_cpf, u.nome as autor_nome, 
                u.email as autor_email, u.foto as autor_foto, 
                u.data_nascimento as autor_data_nascimento,
                u.senha_criptografada as autor_senha_criptografada 
            FROM treinos t
            JOIN usuarios u ON t.usuario = u.id  -- 't.usuario' é o ID do autor
            WHERE t.usuario = :id_autor
            ORDER BY t.data DESC 
        """)
        
        # Exemplo de execução da query (adapte ao seu gerenciamento de conexão)
        try:
            with self._conn.begin(): # Obter uma conexão do engine se self._conn é o engine
                resultados = self._conn.execute(query, {"id_autor": usuario_id_autor}).mappings().all()
        except Exception as e:
            print(f"ERRO ao buscar treinos no repositório: {e}")
            return [] # Retorna lista vazia em caso de erro

        for linha in resultados:
            data_treino_db = linha['treino_data']
            if isinstance(data_treino_db, str): # Converter string para date se necessário
                try:
                    data_treino_db = date.fromisoformat(data_treino_db)
                except ValueError:
                    data_treino_db = None # Ou trate o erro como preferir
            
            data_nasc_autor_db = linha['autor_data_nascimento']
            if isinstance(data_nasc_autor_db, str):
                try:
                    data_nasc_autor_db = date.fromisoformat(data_nasc_autor_db)
                except ValueError:
                    data_nasc_autor_db = None

            autor_do_treino = Usuario(
                id=linha['autor_id'],
                cpf=linha['autor_cpf'],
                nome=linha['autor_nome'],
                email=linha['autor_email'],
                foto=linha['autor_foto'],
                data_nascimento=data_nasc_autor_db,
                senha_criptografada=linha['autor_senha_criptografada'] # Geralmente não é exposta
            )
            treino = Treino(
                id_treino=linha['treino_id'],
                descricao=linha['descricao'],
                duracao=linha['duracao'],
                imagem=linha['treino_imagem'], # Mapeia 'treinos.foto' para 'Treino.imagem'
                usuario=autor_do_treino,
                data_treino=data_treino_db,
                curtidas=linha['treino_curtidas']
            )
            treinos_encontrados.append(treino)
        
        return treinos_encontrados