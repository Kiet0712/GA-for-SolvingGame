from typing import Any
from lib import random,np,plt


class CrosOver(object):
    def __init__(self) -> None:
        pass
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
class OnePoint(CrosOver):
    def __init__(self,rate: float,pop_size: int,elitism: float) -> None:
        super().__init__()
        self.rate = rate
        self.pop_size = pop_size
        self.elitism = elitism
    def __call__(self,father_mother_list: list)-> list:
        number_elitism = int(self.elitism*len(father_mother_list))
        new_gen = []+father_mother_list[:number_elitism]
        while len(new_gen)<self.pop_size:
            father_id = random.randint(0,len(father_mother_list)-1)
            mother_id = random.randint(0,len(father_mother_list)-1)
            while mother_id==father_id:
                mother_id = random.randint(0,len(father_mother_list)-1)
            father = father_mother_list[father_id]
            mother = father_mother_list[mother_id]
            new_gen.append(father[0:int(self.rate*len(father))]+mother[int(self.rate*len(mother)):])
            new_gen.append(mother[0:int(self.rate*len(mother))]+father[int(self.rate*len(father)):])
        return new_gen
class OnePointRandom(CrosOver):
    def __init__(self,pop_size: int,elitism: float) -> None:
        super().__init__()
        self.pop_size = pop_size
        self.elitism = elitism
    def __call__(self,father_mother_list: list)-> list:
        number_elitism = int(self.elitism*len(father_mother_list))
        new_gen = []+father_mother_list[:number_elitism]
        while len(new_gen)<self.pop_size:
            father_id = random.randint(0,len(father_mother_list)-1)
            mother_id = random.randint(0,len(father_mother_list)-1)
            while mother_id==father_id:
                mother_id = random.randint(0,len(father_mother_list)-1)
            father = father_mother_list[father_id]
            mother = father_mother_list[mother_id]
            r = random.uniform(0.1,0.95)
            new_gen.append(father[0:int(r*len(father))]+mother[int(r*len(mother)):])
            new_gen.append(mother[0:int(r*len(mother))]+father[int(r*len(father)):])
        return new_gen
class BLX_alpha1(CrosOver):
    def __init__(self,pop_size: int,alpha: float) -> None:
        super().__init__()
        self.pop_size = pop_size
        self.alpha = alpha
    def __call__(self,father_mother_list: list) -> list:
        new_gen = []+father_mother_list
        while len(new_gen)<self.pop_size:
            father_id = random.randint(0,len(father_mother_list)-1)
            mother_id = random.randint(0,len(father_mother_list)-1)
            while mother_id==father_id:
                mother_id = random.randint(0,len(father_mother_list)-1)
            father = father_mother_list[father_id]
            mother = father_mother_list[mother_id]
            child = []
            for i in range(len(father)):
                max_val = max(father[i],mother[i])
                min_val = min(father[i],mother[i])
                sub = max_val-min_val
                child_i = max(random.uniform(min_val-self.alpha*sub,max_val+self.alpha*sub),1e-6)
                if i>=3:
                    child_i=min(child_i,0.95)
                child.append(child_i)
            new_gen.append(child)
        return new_gen
class BLX_alpha2(CrosOver):
    def __init__(self,pop_size: int,alpha: float) -> None:
        super().__init__()
        self.pop_size = pop_size
        self.alpha = alpha
    def __call__(self,father_mother_list: list) -> list:
        new_gen = []+father_mother_list
        while len(new_gen)<self.pop_size:
            father_id = random.randint(0,len(father_mother_list)-1)
            mother_id = random.randint(0,len(father_mother_list)-1)
            while mother_id==father_id:
                mother_id = random.randint(0,len(father_mother_list)-1)
            father = father_mother_list[father_id]
            mother = father_mother_list[mother_id]
            child1 = []
            child2 = []
            gamma = random.uniform(-self.alpha,1+self.alpha)
            for i in range(len(father)):
                child1_i = max(gamma*father[i]+(1-gamma)*mother[i],1e-6)
                child2_i = max((1-gamma)*father[i]+gamma*mother[i],1e-6)
                if i>=3:
                    child1_i=min(child1_i,0.95)
                    child2_i=min(child2_i,0.95)
                child1.append(child1_i)
                child2.append(child2_i)
            new_gen.append(child1)
            new_gen.append(child2)
        return new_gen
class BLX_alpha3(CrosOver):
    def __init__(self,pop_size: int) -> None:
        super().__init__()
        self.pop_size = pop_size
    def __call__(self,father_mother_list: list) -> list:
        new_gen = []+father_mother_list
        while len(new_gen)<self.pop_size:
            father_id = random.randint(0,len(father_mother_list)-1)
            mother_id = random.randint(0,len(father_mother_list)-1)
            while mother_id==father_id:
                mother_id = random.randint(0,len(father_mother_list)-1)
            father = father_mother_list[father_id]
            mother = father_mother_list[mother_id]
            child1 = []
            child2 = []
            gamma = random.uniform(0,1)
            for i in range(len(father)):
                child1_i = max(0.5*((1+gamma)*father[i]+(1-gamma)*mother[i]),1e-6)
                child2_i = max(0.5*((1-gamma)*father[i]+(1+gamma)*mother[i]),1e-6)
                if i>=3:
                    child1_i=min(child1_i,0.95)
                    child2_i=min(child2_i,0.95)
                child1.append(child1_i)
                child2.append(child2_i)
            new_gen.append(child1)
            new_gen.append(child2)
        return new_gen
class UniformCrossover(CrosOver):
    def __init__(self,pop_size: int) -> None:
        super().__init__()
        self.pop_size = pop_size
    def __call__(self,father_mother_list: list) -> list:
        new_gen = []+father_mother_list
        while len(new_gen)<self.pop_size:
            father_id = random.randint(0,len(father_mother_list)-1)
            mother_id = random.randint(0,len(father_mother_list)-1)
            while mother_id==father_id:
                mother_id = random.randint(0,len(father_mother_list)-1)
            father = father_mother_list[father_id]
            mother = father_mother_list[mother_id]
            child = []
            for i in range(len(father)):
                if random.random()<=0.5:
                    child.append(father[i])
                else:
                    child.append(mother[i])
            new_gen.append(child)
        return new_gen

        
    

