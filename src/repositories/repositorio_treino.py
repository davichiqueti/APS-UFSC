
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
    


    def buscar_treinos_amizades(self, ids_dos_amigos: List[int]) -> List[Treino]:


        if not ids_dos_amigos:
            return []

        treinos_encontrados = []

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
    
    def salvar_curtida(self, treino_id: int) -> bool:

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
        

    def buscar_treinos_amizades_mock(self, ids_dos_amigos_param: Optional[List[int]] = None) -> List[Treino]:
        """
        Retorna uma lista FIXA de treinos mock para fins de teste da UI do feed.
        Opcionalmente, pode filtrar se ids_dos_amigos_param for fornecido.
        """
        print("INFO [RepositorioTreino]: Usando buscar_treinos_amizades_MOCK")
        
        # Define alguns usuários mock aqui mesmo para este método
        # (Você pode ajustar os IDs para corresponder aos IDs dos amigos do seu usuário de teste)
        mock_amigo_1 = Usuario(id=101, cpf="101mock", nome="Amigo Mock A", email="a@mock.com", foto="", data_nascimento=date(1990,1,1), senha_criptografada="mock")
        mock_amigo_2 = Usuario(id=102, cpf="102mock", nome="Amiga Mock B", email="b@mock.com", foto="", data_nascimento=date(1991,1,1), senha_criptografada="mock")
        mock_outro_usuario = Usuario(id=201, cpf="201mock", nome="Outro Usuário Mock C", email="c@mock.com", foto="", data_nascimento=date(1992,1,1), senha_criptografada="mock")

        hoje = date.today()
        lista_interna_mock_treinos = [
            Treino(id_treino=2001, descricao="Treino Mock 1 (Amigo A)", duracao=60, usuario=mock_amigo_1, data_treino=hoje - timedelta(days=1), curtidas=10, imagem="img1.png"),
            Treino(id_treino=2002, descricao="Treino Mock 2 (Amiga B)", duracao=45, usuario=mock_amigo_2, data_treino=hoje - timedelta(days=2), curtidas=25, imagem="img2.png"),
            Treino(id_treino=2003, descricao="Treino Mock 3 (Amigo A)", duracao=30, usuario=mock_amigo_1, data_treino=hoje - timedelta(days=3), curtidas=5, imagem="img3.png"),
            Treino(id_treino=2004, descricao="Treino Mock 4 (Outro Usuário C)", duracao=75, usuario=mock_outro_usuario, data_treino=hoje - timedelta(days=1), curtidas=12, imagem="img4.png"),
            Treino(id_treino=2005, descricao="Treino Mock 5 (Amiga B) - MAIS RECENTE", duracao=50, usuario=mock_amigo_2, data_treino=hoje, curtidas=30, imagem="img5.png"),
        ]

        # Se ids_dos_amigos_param for fornecido, filtra por eles.
        # Caso contrário, para este mock simples, podemos retornar treinos dos amigos 101 e 102.
        if ids_dos_amigos_param is not None:
            treinos_filtrados = [
                t for t in lista_interna_mock_treinos
                if t.usuario and hasattr(t.usuario, 'id') and t.usuario.id in ids_dos_amigos_param
            ]
        else:
            # Para um teste rápido sem depender dos IDs exatos dos amigos do usuário logado,
            # você pode retornar uma lista pré-definida de "treinos de amigos mock".
            # Por exemplo, apenas os treinos de mock_amigo_1 e mock_amigo_2.
            ids_amigos_default_mock = [101, 102]
            treinos_filtrados = [
                t for t in lista_interna_mock_treinos
                if t.usuario and hasattr(t.usuario, 'id') and t.usuario.id in ids_amigos_default_mock
            ]

        # Ordena pela data do treino, do mais recente para o mais antigo
        treinos_filtrados.sort(key=lambda treino: treino.data if treino.data else date.min, reverse=True)
        
        print(f"MOCK [RepositorioTreino.buscar_treinos_amizades_mock]: Retornando {len(treinos_filtrados)} treinos mock.")
        return treinos_filtrados