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

""" utility.search(origem, destino, routers, tables)
exit()

#criando rotas
if not utility.checkRede(origem, destino):
	rota = utility.search(origem, destino, routers)

else:
	rota = [] """

#chamando o ICMP
utility.ICMP(origem, destino, routers, tables, origem, 8, False)

# TODO: testar pra topologia3 -> se funciona ir pra topologiaLoop -> se ficar infinito = duca!
# TODO: implementar time exceed quando for ping E ttl == 0
# TODO: implementar bgl de traceroute

# TODO: CABO FI! :D