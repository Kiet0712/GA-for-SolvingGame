from typing import Any
from lib import random,np,plt


class Selection(object):
    def __init__(self) -> None:
        pass
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
class TopKSelection(Selection):
    def __init__(self,number_parent: int,soft_rate: float) -> None:
        super().__init__()
        self.number_parent = number_parent
        self.soft_rate = soft_rate
    def __call__(self,population: list,fn_score:np.ndarray) -> list:
        argsort = np.argsort(fn_score)[::-1]
        number_good = int(self.number_parent*(1-self.soft_rate))
        parent_list = []
        for i in range(number_good):
            parent_list.append(population[argsort[i]])
        while len(parent_list)<self.number_parent:
            parent_list.append(population[argsort[random.randint(number_good,len(population)-1)]])
        return parent_list