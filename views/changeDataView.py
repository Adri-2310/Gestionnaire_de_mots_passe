"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB
from models.data import Data
import ttkbootstrap.dialogs as dialogs

class ChangeDataView(TopLevelValidateAndCancelForUseDB):
    def __init__(self, master,data_id,board,controller)->None:
        super().__init__(master, "Modifier une données", self.change_data)
        self.board = board
        self.__controller = controller
        self.__data_id = data_id
        data_old = self.__controller.get_one_data(data_id)
        self.var_name.set(data_old.name)
        self.var_username.set(data_old.username)
        self.var_password.set(data_old.password)
        self.var_source.set(data_old.source)

    def change_data(self):
        if self.__controller.modif_data(data_id=self.__data_id,new_data=Data(name=self.var_name.get(),username=self.var_username.get(),password=self.var_password.get(),source=self.var_source.get())):
            dialogs.Messagebox.ok(message="Les informations ont bien été modifiées !",title="Information",parent=self)
            self.board.refresh_data_board_from_db()
            self.destroy()
        else:
            print("la données na pas été modifier")


