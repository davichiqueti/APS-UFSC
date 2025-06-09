from repositories.repositorio_base import RepositorioBase
from models.usuario import Usuario
from sqlalchemy.sql import text
import sqlalchemy
from datetime import date
from typing import List, Optional


class RepositorioUsuario(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def criar(self, user: Usuario):
        query = text("""
        INSERT INTO usuarios (cpf, nome, email, foto, data_nascimento, senha_criptografada)
        VALUES (:cpf, :nome, :email, :foto, :data_nascimento, :senha_criptografada)
        """)
        with self._conn.begin() as transaction:
            self._conn.execute(
                statement=query, 
                parameters={
                    "cpf": user.cpf,
                    "nome": user.nome,
                    "email": user.email,
                    "foto": user.foto,
                    "data_nascimento": user.data_nascimento.isoformat(), 
                    "senha_criptografada": user.senha_criptografada
                }
            )

    def busca_por_nome(self, nome: str) -> Optional[Usuario]:
        usuario_principal_data = None
        query_usuario = text("""
        SELECT
            id, cpf, nome, email, foto, data_nascimento, senha_criptografada
        FROM usuarios
        WHERE nome = :nome
        """)
        
        usuario_id = None
        cpf_usuario = None
        nome_usuario = None
        email_usuario = None
        foto_usuario = None
        data_nasc_usuario = None
        senha_usuario = None
        
        try:
            with self._conn.begin(): 
                result_usuario = self._conn.execute(query_usuario, {"nome": nome})
                usuario_principal_row = result_usuario.fetchone() 
        except Exception as e:
            print(f"ERRO ao buscar usuário principal por nome '{nome}': {e}")
            return None

        if usuario_principal_row:
            usuario_id = usuario_principal_row[0]
            cpf_usuario = usuario_principal_row[1]
            nome_usuario = usuario_principal_row[2]
            email_usuario = usuario_principal_row[3]
            foto_usuario = usuario_principal_row[4]
            data_nasc_usuario_raw = usuario_principal_row[5]
            senha_usuario = usuario_principal_row[6]

            if isinstance(data_nasc_usuario_raw, str):
                try:
                    data_nasc_usuario = date.fromisoformat(data_nasc_usuario_raw)
                except ValueError:
                    print(f"WARN: Formato de data de nascimento inválido para {nome_usuario}: {data_nasc_usuario_raw}")
                    data_nasc_usuario = None
            elif isinstance(data_nasc_usuario_raw, date):
                data_nasc_usuario = data_nasc_usuario_raw
            else:
                data_nasc_usuario = None

            lista_de_amigos_obj: List[Usuario] = []
            if usuario_id is not None: 

                query_amigos = text("""
                SELECT u.id, u.cpf, u.nome, u.email, u.foto, u.data_nascimento, u.senha_criptografada
                FROM usuarios u
                WHERE u.id IN (
                    SELECT destinatario FROM solicitacoes_amizade 
                    WHERE remetente = :user_id AND status = 'aceito'
                    UNION
                    SELECT remetente FROM solicitacoes_amizade 
                    WHERE destinatario = :user_id AND status = 'aceito'
                )
                """)
                
                try:
                    with self._conn.begin(): 
                        result_amigos = self._conn.execute(query_amigos, {"user_id": usuario_id})
                        amigos_rows = result_amigos.fetchall() 
                except Exception as e:
                    print(f"ERRO ao buscar amigos para usuário ID {usuario_id}: {e}")

                    amigos_rows = []

                for amigo_row in amigos_rows:
                    data_nasc_amigo_raw = amigo_row[5]
                    data_nasc_amigo = None
                    if isinstance(data_nasc_amigo_raw, str):
                        try:
                            data_nasc_amigo = date.fromisoformat(data_nasc_amigo_raw)
                        except ValueError:
                            data_nasc_amigo = None
                    elif isinstance(data_nasc_amigo_raw, date):
                        data_nasc_amigo = data_nasc_amigo_raw
                    
                    amigo_obj = Usuario(
                        id=amigo_row[0], cpf=amigo_row[1], nome=amigo_row[2],
                        email=amigo_row[3], foto=amigo_row[4],
                        data_nascimento=data_nasc_amigo, senha_criptografada=amigo_row[6],
                        amizades=[] 
                    )
                    lista_de_amigos_obj.append(amigo_obj)
            
            print(f"DEBUG [RepositorioUsuario.busca_por_nome]: Usuário '{nome_usuario}' encontrado com {len(lista_de_amigos_obj)} amigos.")

            return Usuario(
                id=usuario_id, cpf=cpf_usuario, nome=nome_usuario,
                email=email_usuario, foto=foto_usuario, data_nascimento=data_nasc_usuario,
                senha_criptografada=senha_usuario, amizades=lista_de_amigos_obj
            )
        
        print(f"DEBUG [RepositorioUsuario.busca_por_nome]: Usuário '{nome}' não encontrado.")
        return None
    
    def busca_foto_por_id(self, user_id: int) -> Optional[str]:
        query = text("""
        SELECT foto FROM usuarios WHERE id = :user_id
        """)
        try:
            with self._conn.begin():
                result = self._conn.execute(query, {"user_id": user_id})
                row = result.fetchone()
                if row:
                    return row[0]  # Retorna a foto se encontrada
        except Exception as e:
            print(f"ERRO ao buscar foto do usuário ID {user_id}: {e}")
        return None
    

    def buscar_amizades_aceitas(self, usuario_id):
        query = text("""
            SELECT u.*
            FROM usuarios u
            JOIN solicitacoes_amizade s
              ON ((s.destinatario = u.id OR s.remetente = u.id)
                  AND (s.destinatario = :uid OR s.remetente = :uid)
                  AND u.id != :uid)
            WHERE s.status = 'aceito'
        """)
        result = self._conn.execute(query, {"uid": usuario_id})
        amigos = []
        for row in result.fetchall():
            amigos.append(Usuario(
                id=row[0],
                cpf=row[1],
                nome=row[2],
                email=row[3],
                foto=row[4],
                data_nascimento=row[5],
                senha_criptografada=row[6]
            ))
        return amigos