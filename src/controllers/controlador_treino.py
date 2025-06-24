from datetime import date
from models.treino import Treino
from repositories.repositorio_treino import RepositorioTreino
from views.tela_treino import TelaTreino
from models.usuario import Usuario
from typing import List

class ControladorTreino:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.repositorio = RepositorioTreino()
        self.tela_treino = TelaTreino()

    def abrir_tela_registro(self):
        self.tela_treino.exibir_tela_registro(
            callback_registrar=self.registrar_treino
        )
    
    def pega_usuario_logado(self):
        return self._controlador_sistema.buscar_usuario_logado() 

    def registrar_treino(self, descricao: str, duracao_str: str, imagem_path: str) -> None:
        if not imagem_path:
            raise ValueError("Você deve anexar uma imagem para registrar o treino.")

        usuario = self.pega_usuario_logado()

        try:
            duracao = int(duracao_str) if duracao_str else 0
        except:
            duracao = 0

        treino = Treino(
            descricao=descricao,
            duracao=duracao,
            imagem=imagem_path,
            usuario=usuario,
            data_treino=date.today(),
            curtidas=0
        )
        novo_id = self.repositorio.criar(treino)
        treino.id_treino = novo_id

    
    def obter_treinos_do_usuario(self, usuario: Usuario) -> list[Treino]:

        if not usuario or not hasattr(usuario, 'id') or usuario.id is None:
            print(f"WARN [ControladorTreino]: Tentativa de buscar treinos para usuário inválido: {usuario}")
            return []

        return self.repositorio.buscar_por_usuario_id(usuario.id)
    



    def buscar_treinos_amizades(self, usuario_logado: Usuario) -> List[Treino]:


        if not usuario_logado or not hasattr(usuario_logado, 'amizades') or not usuario_logado.amizades:
            print("DEBUG [ControladorTreino.buscar_treinos_amizades]: Usuário não logado ou sem amigos para buscar treinos.")
            return []

        ids_dos_amigos = [amigo.id for amigo in usuario_logado.amizades if amigo and hasattr(amigo, 'id') and amigo.id is not None]

        if not ids_dos_amigos:
            print("DEBUG [ControladorTreino.buscar_treinos_amizades]: Nenhum ID de amigo válido encontrado.")
            return []
            
        print(f"DEBUG [ControladorTreino.buscar_treinos_amizades]: Buscando treinos para IDs de amigos: {ids_dos_amigos}")


        
        treinos_dos_amigos = self.repositorio.buscar_treinos_amizades(ids_dos_amigos)
       # treinos_dos_amigos = self.repositorio.buscar_treinos_amizades_mock()
        
        if treinos_dos_amigos:
            print(f"DEBUG [ControladorTreino.buscar_treinos_amizades]: {len(treinos_dos_amigos)} treinos de amigos retornados pelo repositório.")
        else:
            print("DEBUG [ControladorTreino.buscar_treinos_amizades]: Nenhum treino de amigo retornado pelo repositório.")
            
        return treinos_dos_amigos
    


    def curtir_treino(self, treino_id: int) -> bool:

        usuario_logado = self.pega_usuario_logado() 
        if not usuario_logado or not hasattr(usuario_logado, 'id') or usuario_logado.id is None:
            print("ERRO [ControladorTreino.curtir_treino]: Usuário não logado. Não é possível curtir.")
            return False 
        
        if treino_id is None:
            print("ERRO [ControladorTreino.curtir_treino]: ID do treino inválido para curtir.")
            return False

        print(f"DEBUG [ControladorTreino.curtir_treino]: Usuário ID {usuario_logado.id} ({usuario_logado.nome if hasattr(usuario_logado, 'nome') else ''}) está tentando curtir treino ID {treino_id}")
        
        sucesso_nova_curtida = self.repositorio.salvar_curtida(treino_id, usuario_logado.id)
        
        if sucesso_nova_curtida:
            print(f"DEBUG [ControladorTreino.curtir_treino]: Nova curtida para treino ID {treino_id} por usuário ID {usuario_logado.id} processada com sucesso pelo repositório.")
        else:
            print(f"INFO [ControladorTreino.curtir_treino]: Ação de curtir para treino ID {treino_id} por usuário ID {usuario_logado.id} não resultou em nova curtida/incremento (já curtido ou erro no repo).")
            
        return sucesso_nova_curtida