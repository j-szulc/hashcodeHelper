from __init__ import *
import random as rnd
import itertools as it

requestInput()

nPizzas, two, three, four = input().split()
pizzas = []
for i in range(int(nPizzas)):
    _, *pizza = input().split()
    pizzas += [tuple(pizza)]
#print(pizzas)

for i in range(42069):
    score = 0
    # S = list(enumerate(
    #     [("onion", "pepper", "olive"), ("mushroom", "tomato", "basil"), ("chicken", "mushroom", "pepper"),
    #      ("tomato", "mushroom", "basil"), ("chicken", "basil")]))  # rodzina podzbiorow z {1..I}
    S = list(enumerate(pizzas))
    S.sort(key=len)
    solution = {2: [], 3: [], 4: []}
    try:
        teams = [(2, int(two)), (3, int(three)), (4, int(four))]
        for (teamSize, teamCount) in teams:
            for i in range(teamCount):
                currentTeam = ()
                for j in range(teamSize):
                    k = rnd.randint(0, len(S) - 1)
                    elem = S.pop(k)
                    currentTeam += (elem,)
                solution[teamSize] += [currentTeam]
                ingredients = list(it.chain(*[pizza[1] for pizza in currentTeam]))
                score+=len(set(ingredients))**2
    except ValueError:
        #print("Run  out of pizzas :(")
        pass
    if shouldSubmit(score):
        startSubmit(score)
        # print(maxScore, maxSolution)
        deliveries = sum((len(x) for x in solution.values()))
        print(deliveries)
        for (teamSize, dels) in solution.items():
            for delivery in dels:
                indexes = [pizza[0] for pizza in delivery]
                print(str(teamSize) + " " + " ".join([str(x) for x in indexes]))
        endSubmit()
        #print(solution)
    #print(maxScore)

