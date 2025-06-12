"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
from models.data import Datas,Data


class ControllersDatas:
    def __init__(self,datas:Datas)->None:
        self.__datas = datas

    def add_data(self,data:Data)->bool:
        return self.__datas.register_data(data)

    def modif_data(self,data_id:int ,new_data:Data)->bool:
        return self.__datas.modify_data(data_id=data_id,new_data=new_data)

    def delete_data(self,data_id:int)->bool:
        return self.__datas.remove_data(data_id)

    def get_all_datas(self)->list[Data]:
        return self.__datas.get_all_Data_in_db()

    def get_one_data(self,data_id:int)->Data:
        return self.__datas.get_one_data_in_db(data_id)