from Population import Population
from CrossOver import CrosOver,OnePoint,OnePointRandom,BLX_alpha1,BLX_alpha2,BLX_alpha3,UniformCrossover
from Selection import Selection,TopKSelection
from Mutation import Mutation,Insertion,Deletion,GeneChange,NormalMutation
from FitnessFunction import FitnessFunction,FitnessFunctionVer2
from lib import np,plt,random,time

class GeneticAlgorithm(object):
    def __init__(self,fn_func: FitnessFunction,selection:Selection,crossover:CrosOver,mutation: list[Mutation])->None:
        self.fn_func = fn_func
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
    def train(self,population_init:list,iter: int,b) -> list:
        population_ans = population_init
        count = 0
        current_val = 0
        for i in range(iter):
            fn_score = self.fn_func(population_ans)
            highest = np.max(fn_score)
            if b==True:
                print('Iter ' + str(i+1) + ':')
                print('Highest acc = ' + str(highest/self.fn_func.maximum_score))
            if highest/self.fn_func.maximum_score==1:
                break
            if highest==current_val:
                count+=1
            else:
                count=0
                current_val=highest
            population_ans = self.selection(population_ans,fn_score)
            population_ans = self.crossover(population_ans)
            for mu in range(len(self.mutation)):
                population_ans = self.mutation[mu](population_ans)
        return population_ans
