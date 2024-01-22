from typing import Any
from lib import random,np,plt
from Individual import Chromosome


class Population(object):
    def __init__(self,min_length: int,max_length: int,vocab: list,size: int) -> None:
        population = []
        for i in range(size):
            population.append(Chromosome(min_length,max_length,vocab).chromosome)
        self.population = population
    def getSize(self)-> int:
        return len(self.population)
    def __call__(self, *args: Any, **kwds: Any) -> list:
        return self.population