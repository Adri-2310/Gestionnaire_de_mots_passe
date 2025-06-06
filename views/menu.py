"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import ttkbootstrap as ttk


class Menu(ttk.Frame):
    def __init__(self,master,treeview):
        super().__init__(master)
        __master = master
        __treeview = treeview
        self.widgets()

    def widgets(self):
        ttk.Button(self, text="Ajouter", command=self.add_data_in_db).pack(side="left")
        change_button = ttk.Button(self, text="modification", command=self.change_data_selected)
        change_button.pack(side="left")
        delete_button = ttk.Button(self, text="supprimer", command=self.delete_data_selected)
        delete_button.pack(side="left")
        show_button = ttk.Button(self, text="Afficher", command=self.show_data_selected)
        show_button.pack(side="left")
        ttk.Button(self,text="Quitter",command=self.master.quit).pack(side="left")

    def add_data_in_db(self):
        pass

    def change_data_selected(self):
        pass

    def delete_data_selected(self):
        pass

    def show_data_selected(self):
        pass