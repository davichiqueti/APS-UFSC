# repositories/repositorio_treino.py

from repositories.repositorio_base import RepositorioBase
from models.treino import Treino
from sqlalchemy.sql import text
import sqlalchemy
from datetime import date
from typing import List

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
    


    def buscar_treinos_amizades(self, ids_dos_amigos: List[int]) -> List[Treino]:

        """
        Busca todos os treinos pertencentes a uma lista de IDs de usuários (amigos).
        Os treinos são ordenados por data (mais recentes primeiro).
        """
        if not ids_dos_amigos:
            return []

        treinos_encontrados = []
        # A cláusula IN é usada para buscar treinos de múltiplos IDs.
        # O formato para `IN` com SQLAlchemy `text()` pode precisar de expansão de bind parameters.
        # Exemplo de construção de query para múltiplos IDs:
        # params = {f"id_amigo_{i}": amigo_id for i, amigo_id in enumerate(ids_dos_amigos)}
        # in_clause = ", ".join([f":id_amigo_{i}" for i in range(len(ids_dos_amigos))])
        # query_str = f""" ... WHERE t.usuario IN ({in_clause}) ... """
        # No entanto, com `execute`, passar uma lista/tupla para um parâmetro usado com `IN` é geralmente suportado.

        query = text(f"""
            SELECT 
                t.id as treino_id, t.descricao, t.duracao, t.foto as treino_imagem, 
                t.data as treino_data, t.curtidas as treino_curtidas,
                u.id as autor_id, u.cpf as autor_cpf, u.nome as autor_nome, 
                u.email as autor_email, u.foto as autor_foto, 
                u.data_nascimento as autor_data_nascimento,
                u.senha_criptografada as autor_senha_criptografada 
            FROM treinos t
            JOIN usuarios u ON t.usuario = u.id
            WHERE t.usuario IN :lista_ids_amigos -- SQLAlchemy expandirá :lista_ids_amigos
            ORDER BY t.data DESC, t.id DESC -- Adicionado t.id para desempate estável
        """)
        
        try:
            with self._conn.begin():
                resultados = self._conn.execute(query, {"lista_ids_amigos": tuple(ids_dos_amigos)}).mappings().all()
        except Exception as e:
            print(f"ERRO ao buscar treinos de lista de usuários no RepositorioTreino: {e}")
            return []

        for linha in resultados:
            data_treino_db = linha['treino_data']; data_nasc_autor_db = linha['autor_data_nascimento']
            # Validação e conversão de datas
            if isinstance(data_treino_db, str): data_treino_db = date.fromisoformat(data_treino_db) if data_treino_db else None
            if isinstance(data_nasc_autor_db, str): data_nasc_autor_db = date.fromisoformat(data_nasc_autor_db) if data_nasc_autor_db else None

            autor = Usuario(id=linha['autor_id'], cpf=linha['autor_cpf'], nome=linha['autor_nome'],
                           email=linha['autor_email'], foto=linha['autor_foto'],
                           data_nascimento=data_nasc_autor_db, senha_criptografada=linha['autor_senha_criptografada'])
            treino = Treino(id_treino=linha['treino_id'], descricao=linha['descricao'], duracao=linha['duracao'],
                           imagem=linha['treino_imagem'], usuario=autor, data_treino=data_treino_db,
                           curtidas=linha['treino_curtidas'])
            treinos_encontrados.append(treino)
        
        return treinos_encontrados
    
    def salvar_curtida(self, treino_id: int) -> bool: # Seu método existente
        # ... (implementação para salvar curtida) ...
        query = text("""
            UPDATE treinos SET curtidas = curtidas + 1
            WHERE id = :treino_id
        """)
        try:
            with self._conn.begin():
                result = self._conn.execute(query, {"treino_id": treino_id})
                return result.rowcount > 0
        except Exception as e:
            print(f"ERRO ao salvar curtida no RepositorioTreino: {e}")
            return False