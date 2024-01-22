from GeneticAlgorithm import *
from ReachTheFlagGameCode import Game
import time
import joblib
import pickle
vocab = ['w','a','s','d']
def calc_max_length(map_array:np.ndarray):
    count = 0
    y,x = np.where(map_array==-2)
    flag_y,flag_x = np.where(map_array==-3)
    y = np.concatenate([y,flag_y],axis=0)
    x = np.concatenate([x,flag_x],axis=0)
    y = y.reshape(-1,1)
    x = x.reshape(-1,1)
    y_left,x_left = y,x-1
    y_right,x_right = y,x+1
    y_bottom,x_bottom = y-1,x
    y_up,x_up = y+1,x
    y_near = np.concatenate([y_left,y_right,y_bottom,y_up],axis=1)
    x_near = np.concatenate([x_left,x_right,x_bottom,x_up],axis=1)
    for i in range(y.shape[0]):
        for j in range(4):
            if y_near[i,j]<0 or y_near[i,j]>=map_array.shape[0] or x_near[i,j]<0 or x_near[i,j]>=map_array.shape[1]:
                continue
            if map_array[y_near[i,j],x_near[i,j]]==1 or map_array[y_near[i,j],x_near[i,j]]==2:
                count+=map_array[y_near[i,j],x_near[i,j]]
    map_array = map_array.reshape(-1,)
    return map_array[map_array==1].shape[0]+map_array[map_array==2].shape[0]*2+count
def run_with_level(level,hyper_list,run_visualize=False,printable=False):
    np.random.seed(7122004)
    random.seed(7122004)
    map_array = np.load('Round_' + str(level)+'_map.npy')
    flag_ans_player_pos_arr = np.load('PlayerAndFlaginitPos.npy')
    flag_pos = (flag_ans_player_pos_arr[level-1,2],flag_ans_player_pos_arr[level-1,3])
    player_init_pos = (flag_ans_player_pos_arr[level-1,0],flag_ans_player_pos_arr[level-1,1])
    fn_func = FitnessFunctionVer2(map_array,player_init_pos,flag_pos,hyper_list[0:3])
    min_length = fn_func.weightmap(map_array)
    max_length = calc_max_length(map_array)
    pop_size = 2000
    remain_parent = 800
    soft_rate = hyper_list[3]
    population_init = Population(min_length,max_length,vocab,pop_size)
    selection = TopKSelection(remain_parent,soft_rate)
    crossover = OnePointRandom(pop_size,hyper_list[4])
    mutation = [
        Insertion(hyper_list[5],vocab,hyper_list[6],max_length),
        Deletion(hyper_list[7],vocab,hyper_list[8],min_length),
        GeneChange(hyper_list[9],vocab,hyper_list[10])
    ]
    ga = GeneticAlgorithm(fn_func,selection,crossover,mutation)
    population_ans = ga.train(population_init.population,4000,printable)
    score_ans = fn_func(population_ans)
    print('Level = ' + str(level) + ':')
    print('Highest acc = ' + str(np.max(score_ans)/fn_func.maximum_score))
    # print('Best solution = ' + str(population_ans[np.argmax(score_ans)]))
    if run_visualize==True:
        game_mode = Game(map_array,player_init_pos,50,(600,600))
        game_mode.geneticAlgorithmPlay(population_ans[np.argmax(score_ans)])
        #game_mode.game_loop()
    return np.max(score_ans)/fn_func.maximum_score
def init_pop(pop_size):
    pop = []
    for i in range(pop_size):
        chromosome = []
        for j in range(11):
            if j < 3:
                chromosome.append(random.uniform(0,1))
            else:
                chromosome.append(random.uniform(1e-6,0.95))
        pop.append(chromosome)
    return pop
old_hyperparameter = []
old_score = []
def full_level(hyper_parameter,printable=False,visualize=False,win_level_check=False,level_list=[*range(1,65)]):
    if win_level_check==False:
        for i in range(len(old_hyperparameter)):
            if old_hyperparameter[i]==hyper_parameter:
                return old_score[i]
    win_level = []
    score = 0
    for i in level_list:
        level_i_score = run_with_level(i,hyper_parameter,visualize,printable)
        if level_i_score==1:
            win_level.append(i)
        score+=level_i_score
    print('Average score level = ' + str(score/64))
    print('Number win level = ' + str(len(win_level)))
    fn_score = 0.25*score/64+0.75*len(win_level)/64
    if win_level_check==True:
        return fn_score,win_level
    else:
        old_hyperparameter.append(hyper_parameter)
        old_score.append(fn_score)
        return fn_score
def find_for_64_level():
    pop_size = 32
    remain_parent = 13
    number_generation = 10
    crossover = BLX_alpha1(pop_size,0.5)
    mutation = NormalMutation(4e-2,1,0.15)
    selection = TopKSelection(remain_parent,0.25)
    with open("hyperparam_pop_small_generation.pkl", "rb") as f:
    # Unpickle the list of lists from the file
        pop = pickle.load(f)
    print(len(pop))
    f.close()
    for i in range(number_generation):
        print('Generation ' + str(i+1) + ':')
        fn_score = joblib.Parallel(-1)(joblib.delayed(full_level)(x) for x in pop)
        fn_score = np.array(fn_score)
        print('Best score = ' + str(np.max(fn_score)))
        print('Best hyper = ' + str(pop[np.argmax(fn_score)]))
        if np.max(fn_score)==1:
            win_hyper = pop[np.argmax(fn_score)]
            print('Win hyper = '+ str(win_hyper))
            score,win_level = full_level(win_hyper,False,True,True)
            return win_hyper,win_level,score,np.argmax(fn_score)
        pop = selection(pop,fn_score)
        pop = crossover(pop)
        pop = mutation(pop)
        with open("hyperparam_pop_small_generation.pkl", "wb") as f:
            # Pickle the list of lists to the file
            pickle.dump(pop, f)
    win_hyper = pop[np.argmax(fn_score)]
    print('Best hyper = '+ str(win_hyper))
    score,win_level = full_level(win_hyper,False,True,True)
    return win_hyper,win_level,score,np.argmax(fn_score)
# best_hyper_score,win_level,score,idx = find_for_64_level()
# print('idx of best hyper score = ' + str(idx))
# print('Best hyper score = ' + str(best_hyper_score))
# print('Best score = ' + str(score))
# print('Best win level = ' + str(win_level))
# print('Best number level pass = ' + str(len(win_level)))
# havenot_win = list(set([*range(1,65)]).difference(set([1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 14, 15, 25, 26, 28, 34, 44, 45, 49])))
best_win_list = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 14, 15, 25, 26, 28, 34, 44, 45, 49]
print(run_with_level(11,[0.38611523304420414, 0.00341861243229647, 0.1486385421749012, 0.4244501893948795, 0.9259517646994223, 0.4864685675347392, 0.06369979812062912, 0.5587246451571839, 0.44074726654088137, 0.49409848850181576, 0.8459500653887697],True,True))