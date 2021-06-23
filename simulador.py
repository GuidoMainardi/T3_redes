import utility
import sys

file = sys.argv[1]
instruction = sys.argv[2]
params = sys.argv[3:]

nodes, routers, tables = utility.parser(file)

#pergunta: len(params) == 2 sempre?
#separando os nodes que vamos usar
origem = nodes[int(params[0].split("n")[-1])-1]
destino = nodes[int(params[1].split("n")[-1])-1]


#chamando o ICMP
if instruction == "ping":
	utility.ICMP(origem, destino, routers, tables, origem, 8, 0, instruction)

else:
	utility.ICMP(origem, destino, routers, tables, origem, 1, 0, instruction)

# TODO: implementar bgl de traceroute

# TODO: CABO FI! :D