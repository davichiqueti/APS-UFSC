
from repositories.repositorio_base import RepositorioBase
from models.treino import Treino
from sqlalchemy.sql import text
import sqlalchemy
from datetime import date, timedelta 
from typing import List, Optional

from models.usuario import Usuario

class RepositorioTreino(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def criar(self, treino: Treino) -> None:
        query = text("""
        INSERT INTO treinos (descricao, imagem, duracao, usuario, curtidas, data)
        VALUES (:descricao, :imagem, :duracao, :usuario, :curtidas, :data)
        """)
        with self._conn.begin() as transaction:
            self._conn.execute(
                statement = query,
                parameters = {
                    "descricao": treino.descricao,
                    "imagem": treino.imagem, 
                    "duracao": treino.duracao,
                    "usuario": treino.usuario.id,
                    "curtidas": treino.curtidas,
                    "data": treino.data.isoformat() if treino.data else None
                    }
            )


    def buscar_por_usuario_id(self, usuario_id_autor: int) -> list[Treino]:

        treinos_encontrados = []

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
                senha_criptografada=linha['autor_senha_criptografada']
            )
            treino = Treino(
                id_treino=linha['treino_id'],
                descricao=linha['descricao'],
                duracao=linha['duracao'],
                imagem=linha['treino_imagem'],
                usuario=autor_do_treino,
                data_treino=data_treino_db,
                curtidas=linha['treino_curtidas']
            )
            treinos_encontrados.append(treino)
        
        return treinos_encontrados
    

    def buscar_treinos_amizades(self, ids_dos_amigos: List[int]) -> List[Treino]: # Nome conforme seu código
        """
        Busca todos os treinos pertencentes a uma lista de IDs de usuários (amigos).
        Os treinos são ordenados por data (mais recentes primeiro).
        """
        if not ids_dos_amigos:
            return []

        treinos_encontrados = []
        # CORREÇÃO: Selecionar t.imagem como treino_imagem
        query = text(f"""
            SELECT 
                t.id_treino as treino_id, t.descricao, t.duracao, t.imagem as treino_imagem, 
                t.data as treino_data, t.curtidas as treino_curtidas,
                u.id as autor_id, u.cpf as autor_cpf, u.nome as autor_nome, 
                u.email as autor_email, u.foto as autor_foto, 
                u.data_nascimento as autor_data_nascimento,
                u.senha_criptografada as autor_senha_criptografada 
            FROM treinos t
            JOIN usuarios u ON t.usuario = u.id
            WHERE t.usuario IN :lista_ids_amigos
            ORDER BY t.data DESC, t.id_treino DESC -- t.id_treino para desempate estável
        """)
        
        try:
            # Assumindo que self._conn é uma conexão e você gerencia transações com begin()
            # Se self._conn for um engine, seria: with self._conn.connect() as connection:
            with self._conn.begin(): 
                resultados = self._conn.execute(query, {"lista_ids_amigos": tuple(ids_dos_amigos)}).mappings().all()
        except Exception as e:
            print(f"ERRO ao buscar treinos de lista de usuários no RepositorioTreino: {e}")
            return []

        for linha in resultados:
            data_treino_db = linha['treino_data']
            if isinstance(data_treino_db, str): data_treino_db = date.fromisoformat(data_treino_db) if data_treino_db else None
            
            data_nasc_autor_db = linha['autor_data_nascimento']
            if isinstance(data_nasc_autor_db, str): data_nasc_autor_db = date.fromisoformat(data_nasc_autor_db) if data_nasc_autor_db else None

            autor = Usuario(id=linha['autor_id'], cpf=linha['autor_cpf'], nome=linha['autor_nome'],
                           email=linha['autor_email'], foto=linha['autor_foto'],
                           data_nascimento=data_nasc_autor_db, senha_criptografada=linha['autor_senha_criptografada'])
            treino = Treino(id_treino=linha['treino_id'], descricao=linha['descricao'], duracao=linha['duracao'],
                           imagem=linha['treino_imagem'], # Corretamente mapeado de t.imagem
                           usuario=autor, data_treino=data_treino_db,
                           curtidas=linha['treino_curtidas'])
            treinos_encontrados.append(treino)
        
        return treinos_encontrados
    
    def salvar_curtida(self, treino_id: int, usuario_id: int) -> bool:

        query_inserir_curtida_individual = text("""
            INSERT INTO treino_curtidas (usuario_id, treino_id, data_curtida)
            VALUES (:user_id, :train_id, CURRENT_TIMESTAMP)
            ON CONFLICT (usuario_id, treino_id) DO NOTHING; 
        """)
        # ON CONFLICT DO NOTHING é específico do PostgreSQL. Adapte se usar outro banco.

        query_incrementar_contador_geral = text("""
            UPDATE treinos SET curtidas = curtidas + 1
            WHERE id_treino = :train_id 
        """) # Usa id_treino conforme sua tabela treinos
        
        try:
            with self._conn.begin() as transaction: # Garante atomicidade
                result_insert_individual = self._conn.execute(
                    query_inserir_curtida_individual, 
                    {"user_id": usuario_id, "train_id": treino_id}
                )
                
                # result_insert_individual.rowcount será 1 se uma nova linha foi inserida,
                # e 0 se ON CONFLICT DO NOTHING foi acionado (curtida já existia).
                if result_insert_individual.rowcount > 0:
                    # Nova curtida, então incrementa o contador geral
                    self._conn.execute(query_incrementar_contador_geral, {"train_id": treino_id})
                    print(f"DEBUG [RepositorioTreino.salvar_curtida]: Novo like de usuario {usuario_id} para treino {treino_id} inserido e contador incrementado.")
                    return True # Sucesso, nova curtida
                else:
                    # O usuário já havia curtido este treino.
                    print(f"INFO [RepositorioTreino.salvar_curtida]: Usuário {usuario_id} já havia curtido o treino {treino_id}. Contador não alterado.")
                    return False # Não foi uma "nova" curtida para o contador geral
            # 'with self._conn.begin()' faz commit ou rollback automaticamente.
                
        except Exception as e:
            print(f"ERRO GERAL ao salvar curtida no RepositorioTreino para treino {treino_id} por usuario {usuario_id}: {e}")
            return False # Erro na operação