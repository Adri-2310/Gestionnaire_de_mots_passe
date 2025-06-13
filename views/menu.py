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

    def __init__(self, master, board):
        """
        Initialise le menu principal.

        Args:
            master: Le widget parent.
            board: Le widget Treeview pour afficher les données.
        """
        super().__init__(master)
        self.__master = master
        self.board = board
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
            ("AFFICHER", self.show_data_selected),
            ("QUITTER", self.__master.quit)
        ]

        for text, command in buttons_config:
            button = ttk.Button(self, text=text, command=command, style="AllButton.TButton")
            button.pack(side="left", padx=5, pady=10)

    def add_data(self):
        """
        Ouvre la vue pour ajouter des données.
        """
        AddDataView(self.__master, self.__controller, self.board)

    def change_data_selected(self):
        """
        Ouvre la vue pour modifier les données sélectionnées.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("Aucune donnée sélectionnée")

            ChangeDataView(master=self.__master, board=self.board,data_id=int(self.board.board.selection()[0]),controller=self.__controller)
        except IndexError:
            print("Veuillez selectionnez un élément dans le tableau")

    def delete_data_selected(self):
        """
        Supprime les données sélectionnées dans le Treeview.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("Aucune donnée sélectionnée")
            # ajout une boite de dialoque pour confirmer la suppression
            selected_item = self.board.board.selection()
            if selected_item:
                if self.__controller.delete_data(data_id=int(selected_item[0])):
                    print("la données a bien été supprimé")
                    self.board.board.delete(selected_item)
        except IndexError:
            print("Veuillez selectionnez un élément dans le tableau")

    def show_data_selected(self):
        """
        Ouvre la vue pour afficher les données sélectionnées.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("Aucune donnée sélectionnée")

            ShowDataView(master=self.__master, board=self.board,controller=self.__controller)
        except IndexError:
            print("Veuillez selectionnez un élément dans le tableau")

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
