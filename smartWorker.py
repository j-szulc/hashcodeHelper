import random as rnd
import itertools as it
from simanneal import *
from __init__ import *

requestInput()

nPizzas, two, three, four = input().split()
pizzas = []
for i in range(int(nPizzas)):
    _, *pizza = input().split()
    pizzas += [tuple(pizza)]


# print(pizzas)

def rndSol():
    score = 0
    # S = list(enumerate(
    #     [("onion", "pepper", "olive"), ("mushroom", "tomato", "basil"), ("chicken", "mushroom", "pepper"),
    #      ("tomato", "mushroom", "basil"), ("chicken", "basil")]))  # rodzina podzbiorow z {1..I}
    S = list(enumerate(pizzas))
    solution = []
    teams = [(2, int(two)), (3, int(three)), (4, int(four))]
    for (teamSize, teamCount) in teams:
        for i in range(teamCount):
            currentTeam = []
            try:
                for j in range(teamSize):
                    k = rnd.randint(0, len(S) - 1)
                    elem = S.pop(k)
                    currentTeam.append(elem)
            except ValueError:
                # print("Run  out of pizzas :(")
                pass
            solution += [currentTeam]
            ingredients = list(it.chain(*[pizza[1] for pizza in currentTeam]))
            score += len(set(ingredients)) ** 2
    return [solution, score]


class Smart(Annealer):

    def move(self):
        try:
            i = rnd.randint(0, len(self.state[0]) - 1)
            j = rnd.randint(0, len(self.state[0]) - 1)
            old = 0
            for x in [i, j]:
                ingredients = set(it.chain(*[pizza[1] for pizza in self.state[0][x]]))
                old += len(ingredients) ** 2
            ii = rnd.randint(0, len(self.state[0][i]) - 1)
            p = self.state[0][i][ii]
            jj = rnd.randint(0, len(self.state[0][j]) - 1)
            q = self.state[0][j][jj]
            self.state[0][i].pop(ii)
            self.state[0][i].append(q)
            self.state[0][j].pop(jj)
            self.state[0][j].append(p)
            new = 0
            for x in [i, j]:
                ingredients = set(it.chain(*[pizza[1] for pizza in self.state[0][x]]))
                new += len(ingredients) ** 2
            self.state[1] += new - old
        except ValueError:
            pass

    def energy(self):
        print(-self.state[1], file=sys.stderr)
        return -self.state[1]
        e = 0
        for team in self.state[0]:
            ingredients = set(it.chain(*[pizza[1] for pizza in team]))
            e += len(ingredients) ** 2
        # print(e,self.state)
        return -e


#     if score > maxScore:
#         maxScore = score
#         maxSolution = solution
#         #print(solution)
#     #print(maxScore)
# #print(maxScore, maxSolution)

while True:
    s = rndSol()
    ss = Smart(s)
    ans = ss.anneal()
    sol = ans[0][0]
    score = -ans[1]
    if (shouldSubmit(score)):
        startSubmit(score)
        deliveries = sum((len(x) for x in sol))
        print(deliveries)
        for delivery in sol:
            teamSize = len(delivery)
            if teamSize == 0:
                continue
            indexes = [pizza[0] for pizza in delivery]
            print(str(teamSize) + " " + " ".join([str(x) for x in indexes]))
        endSubmit()
