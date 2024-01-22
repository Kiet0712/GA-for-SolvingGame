from typing import Any
from lib import random,np,plt


class Mutation(object):
    def __init__(self) -> None:
        pass
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
class GeneChange(Mutation):
    def __init__(self,rate_per_bit: float,vocab: list,elitism: float) -> None:
        self.rate_per_bit = rate_per_bit
        self.vocab = vocab
        self.elitism = elitism
    def __call__(self,population:list) -> list:
        number_none_mutation = int(self.elitism*len(population))
        for i in range(number_none_mutation,len(population)):
            for j in range(len(population[i])):
                if random.random() <= self.rate_per_bit:
                    change_value = random.choice(self.vocab)
                    while change_value==population[i][j]:
                        change_value = random.choice(self.vocab)
                    population[i][j]=change_value
        return population
class Insertion(Mutation):
    def __init__(self,rate: float,vocab: list,elitism: float,max_length: int) -> list:
        self.rate = rate
        self.vocab = vocab
        self.elitism = elitism
        self.max_length = max_length
    def __call__(self,population:list) -> None:
        number_none_mutation = int(self.elitism*len(population))
        for i in range(number_none_mutation,len(population)):
            len_chromosome_i = len(population[i])
            if random.random()<=self.rate and len_chromosome_i<self.max_length:
                population[i].insert(random.randint(0,len_chromosome_i-1),random.choice(self.vocab))
        return population
class Deletion(Mutation):
    def __init__(self,rate: float,vocab: list,elitism: float,min_length: int) -> None:
        self.rate = rate
        self.vocab = vocab
        self.elitism = elitism
        self.min_length = min_length
    def __call__(self,population:list) -> list:
        number_none_mutation = int(self.elitism*len(population))
        for i in range(number_none_mutation,len(population)):
            len_chromosome_i = len(population[i])
            if random.random()<=self.rate and len_chromosome_i>self.min_length:
                population[i].pop(random.randint(0,len_chromosome_i-1))
        return population
class NormalMutation(Mutation):
    def __init__(self,mutation_rate: float,rate: float,elitism: float) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate
        self.rate = rate
        self.elitism = elitism
    def __call__(self,population:list) -> list:
        number_none_mutation = int(self.elitism*len(population))
        for i in range(number_none_mutation,len(population)):
            for j in range(len(population[i])):
                rd_vec = np.random.normal(0,1,(len(population[i]),))
                if random.random()<=self.rate:
                    population[i][j]+=self.mutation_rate*rd_vec[j]
                    population[i][j] = max(population[i][j],1e-6)
                    if j>=3:
                        population[i][j]=min(population[i][j],0.95)
        return population