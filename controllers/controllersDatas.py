"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from models.data import Datas,Data


class ControllersDatas:
    def __init__(self,datas:Datas):
        self.__datas = datas

    def add_data(self,data:Data):
        return self.__datas.register_data(data)
