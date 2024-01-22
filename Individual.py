from typing import Any
from lib import random,np,plt

class Chromosome(object):
    def __init__(self,min_length: int,max_length: int,vocab: list) -> None:
        r = random.randint(min_length,max_length)
        chromosome = []
        for i in range(r):
            chromosome.append(random.choice(vocab))
        self.chromosome = chromosome
    def __call__(self, *args: Any, **kwds: Any) -> list:
        return self.chromosome