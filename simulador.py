import utility
import sys

file = sys.argv[1]
instruction = sys.argv[2]
params = sys.argv[3:]

nodes, routers, tables = utility.parser(file)

utility.imprime(nodes)
utility.imprime(routers)
utility.imprime(tables)