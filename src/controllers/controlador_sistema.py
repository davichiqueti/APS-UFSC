#from views.tela_sistema import TelaSistema
from controllers.controlador_usuario import ControladorUsuario


class ControladorSistema:
    def __init__(self):
        #self.tela_sistema = TelaSistema()
        self.controlador_usuario = ControladorUsuario()

    def abrir_tela_usuario(self):
        self.controlador_usuario.iniciar()

    def iniciar(self):
        self.controlador_usuario.abrir_tela_login()
