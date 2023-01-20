from common import *
from tree_search import *
from rush import *

map = Map("3 ooBoooooBooCAABooCoooooooooooooooooo 62")


domain = RushHour(map)
problem = SearchProblem(domain, map)

tree = SearchTree(problem, 'depth')

print(tree.search(limit=10))
