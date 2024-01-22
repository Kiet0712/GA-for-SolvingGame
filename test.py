import pickle

with open("hyperparam_pop.pkl", "rb") as f:
    # Unpickle the list of lists from the file
        pop = pickle.load(f)
f.close()
for i in range(len(pop)):
    print('chromosome ' + str(i+1) + ' = ' + str(pop[i]))