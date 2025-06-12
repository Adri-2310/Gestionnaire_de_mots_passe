"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB
from models.data import Data


class AddDataView(TopLevelValidateAndCancelForUseDB):
    def __init__(self,master,controllers,board):
        super().__init__(master,"Ajouter une données",self.command)
        self.__master = master
        self.board = board
        self.__controllers = controllers

    def command(self):
        if self.__controllers.add_data(Data(self.var_name.get(),self.var_username.get(),self.var_password.get(),self.var_source.get())):
            print("la données a bien été enregsitré")
            self.board.refresh_data_board_from_db()
            self.destroy()
        else:
            print("la données existe déja")

