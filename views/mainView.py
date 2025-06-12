"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import ttkbootstrap as ttk
from views.menu import Menu
from views.boardView import BoardView
from controllers.controllersDatas import ControllersDatas
from models.data import Datas


class MainWindow(ttk.Window):
    def __init__(self,title:str,path_db:str):
        super().__init__(themename="superhero")
        self.title(title)
        self.resizable(False,False)
        self.place_window_center()
        __treeview = BoardView(self)
        __treeview.controller = ControllersDatas(Datas(path_db))
        __treeview.grid(row=1,column=0,sticky='nsew',padx=10,pady=8)
        __menu=Menu(self, __treeview.board)
        __menu.controller = ControllersDatas(Datas(path_db))
        __menu.grid(row=0, column=0, sticky='nsew',padx=10,pady=8)
        self.mainloop()





