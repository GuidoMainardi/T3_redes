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

#criando rotas
rota = utility.search(origem, destino, routers)
#chamando o ICMP
utility.ICMP(origem, destino, rota, routers)




#TODO: terminar a função search do utility (com mais de um roteador linkado ela certamente n vai funcionar)
#TODO: função ARP provavelmente não funciona quando ambos parametros são roteadores
#TODO: fazer um get ip em router pra n ficar um lixo