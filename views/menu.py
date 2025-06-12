"""
Module pour le menu principal de l'application de gestion des mots de passe.
Auteur : Adrien Mertens
Version : 1.0
"""

import ttkbootstrap as ttk
from views.addDataView import AddDataView
from views.changeDataView import ChangeDataView
from views.showDataView import ShowDataView

class Menu(ttk.Frame):
    """
    Une classe pour représenter le menu principal de l'application.
    Ce menu permet d'ajouter, modifier, supprimer, afficher des données et quitter l'application.
    """

    def __init__(self, master, treeview):
        """
        Initialise le menu principal.

        Args:
            master: Le widget parent.
            treeview: Le widget Treeview pour afficher les données.
        """
        super().__init__(master)
        self.__master = master
        self.__treeview = treeview
        self.__controller = None
        self.widgets()

    def widgets(self):
        """
        Crée et configure les widgets du menu.
        """
        # Créer un style personnalisé pour chaque bouton
        style = ttk.Style()
        style.configure('AllButton.TButton', borderwidth=1, relief="solid", bordercolor="#4e5d6c")
        style.map('AllButton.TButton',
                  background=[('active', '#ABB6C2'), ('!active', '#4e5d6c')],
                  foreground=[('active', 'black'), ('!active', 'white')])

        # Configuration des boutons
        buttons_config = [
            ("AJOUTER", self.add_data),
            ("MODIFICATION", self.change_data_selected),
            ("SUPPRIMER", self.delete_data_selected),
            ("AFFICHIER", self.show_data_selected),
            ("QUITTER", self.__master.quit)
        ]

        for text, command in buttons_config:
            button = ttk.Button(self, text=text, command=command, style="AllButton.TButton")
            button.pack(side="left", padx=5, pady=10)

    def add_data(self):
        """
        Ouvre la vue pour ajouter des données.
        """
        AddDataView(self.__master,self.__controller)

    def change_data_selected(self):
        """
        Ouvre la vue pour modifier les données sélectionnées.
        """
        ChangeDataView(self.__master, self.__treeview)

    def delete_data_selected(self):
        """
        Supprime les données sélectionnées dans le Treeview.
        """
        selected_item = self.__treeview.selection()
        if selected_item:
            self.__treeview.delete(selected_item)

    def show_data_selected(self):
        """
        Ouvre la vue pour afficher les données sélectionnées.
        """
        ShowDataView(self.__master, self.__treeview)

    @property
    def controller(self):
        """
        Obtient le contrôleur associé à ce menu.

        Returns:
            Le contrôleur associé.

        Raises:
            AttributeError: Si le contrôleur n'est pas défini, quitte l'application.
        """
        try:
            return self.__controller
        except AttributeError:
            self.__master.quit()

    @controller.setter
    def controller(self, controller):
        """
        Définit le contrôleur associé à ce menu.

        Args:
            controller: Le contrôleur à associer.
        """
        self.__controller = controller
