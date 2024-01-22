from typing import Any
from lib import random,np,plt
import time
class FitnessFunction(object):
    def __init__(self,map_array:np.ndarray,player_init_pos: tuple,flag_pos: tuple,lamda_list: list) -> None:
        self.map_array = map_array
        self.player_init_pos = player_init_pos
        self.flag_pos = flag_pos
        self.lamda_list = lamda_list
        self.weightinitmap = self.weightmap(self.map_array)
        self.maximum_score = 0
    def weightmap(self,map_array: np.ndarray) -> int:
        map_array = map_array.reshape(-1,)
        return map_array[map_array==1].shape[0]+map_array[map_array==2].shape[0]*2
    def change_block(self,value):
        if value==-2 or value==-3:
            return value
        elif value==2:
            return 1
        elif value==1:
            return -1
        else:
            return None
    def distance(self,a: tuple,b: tuple):
        x_dis = b[1]-a[1]
        y_dis = b[0]-a[0]
        return (x_dis**2+y_dis**2)**0.5
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
class FitnessFunctionVer2(FitnessFunction):
    def __init__(self, map_array: np.ndarray, player_init_pos: tuple, flag_pos: tuple, lamda_list: list) -> None:
        super().__init__(map_array, player_init_pos, flag_pos, lamda_list)
        self.maximum_score = self.lamda_list[0]*self.weightmap(self.map_array)**2
    def calc_value(self,chromosome_i):
        map_temp = self.map_array.copy()
        y,x = self.player_init_pos
        y_size = map_temp.shape[0]
        x_size = map_temp.shape[1]
        for j in range(len(chromosome_i)):
            new_x = x
            new_y = y
            if chromosome_i[j]=='w':
                new_y-=1
            elif chromosome_i[j]=='s':
                new_y+=1
            elif chromosome_i[j]=='a':
                new_x-=1
            elif chromosome_i[j]=='d':
                new_x+=1
            if new_x<0 or new_x >= x_size or new_y<0 or new_y>=y_size:
                x=new_x
                y=new_y
                break
            if map_temp[new_y,new_x]==-1:
                x=new_x
                y=new_y
                break
            map_temp[y,x]=self.change_block(map_temp[y,x])
            x=new_x
            y=new_y
        block_score = self.weightinitmap-self.weightmap(map_temp)
        remain_step_move = len(chromosome_i)-j-1
        distance = self.distance((y,x),self.flag_pos)
        score = self.lamda_list[0]*block_score**2-self.lamda_list[1]*remain_step_move**2-self.lamda_list[2]*distance**2
        return score
    def __call__(self,population: list)->np.ndarray:
        return np.array([self.calc_value(chromosome) for chromosome in population])