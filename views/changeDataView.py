"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB
class ChangeDataView(TopLevelValidateAndCancelForUseDB):
    def __init__(self, master,selected_data_in_treeview):
        super().__init__(master, "Modifier une données", print("test change data in db"))
        self.__selected_data_in_treeview = selected_data_in_treeview

        # création du controller pour le placer dans command_for_validateButton et lui donner
        # en paramètre les la var de ttk


