"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB
from models.data import Data
import ttkbootstrap.dialogs as dialogs


class AddDataView(TopLevelValidateAndCancelForUseDB):
    def __init__(self,master,controller,board):
        super().__init__(master,"Ajouter une données",self.command)
        self.__master = master
        self.board = board
        self.__controller = controller

    def command(self):
        if self.__controller.add_data(Data(self.var_name.get(),self.var_username.get(),self.var_password.get(),self.var_source.get())):
            dialogs.Messagebox.ok(message="L'enregistrement a bien été effectué !",title="Information",parent=self)
            self.board.refresh_data_board_from_db()
            self.destroy()
        else:
            print("la données existe déja")

