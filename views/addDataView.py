"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB


class AddDataView(TopLevelValidateAndCancelForUseDB):
    def __init__(self,master):
        super().__init__(master,"Ajouter une données",print("test add data in db"))

        # création du controller pour le placer dans command_for_validateButton et lui donner
        # en paramètre les la var de ttk