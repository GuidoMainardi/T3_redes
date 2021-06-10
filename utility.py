import re
from enum import Enum
import Node, Router, Router_table

class Flag(Enum):
	ARP_req = 1
	ARP_reply = 2
	ICMP_req = 3
	ICMP_reply = 4
	ICMP_time = 5

def imprime(str, src_name = 0, src_ip = 0, dst_ip = 0, dst_name = 0, ttl = 8, mac = 0):
	if str == Flag.ARP_req:
		print(f"Note over {src_name} : ARP Request<br/>Who has {dst_ip}? Tell {src_ip}")

	elif str == Flag.ARP_reply:
		print(f"{src_name} ->> {dst_name} : ARP Reply<br/>{src_ip} is at {mac}")

	elif str == Flag.ICMP_req:
		print(f"{src_name} ->> {dst_name} : ICMP Echo Request<br/>src={src_ip} dst={dst_ip} ttl={ttl}")

	elif str == Flag.ICMP_reply:
		print(f"{src_name} ->> {dst_name} : ICMP Echo Reply<br/>src={src_ip} dst={dst_ip} ttl={ttl}")

	elif str == Flag.ICMP_time:
		print(f"{src_name} ->> {dst_name} : ICMP Time Exceeded<br/>src={src_ip} dst={dst_ip} ttl={ttl}")

	else:
		print("ERRO :(")

	return

#verifica se "n1" e "n2" sao da mesma rede, retorna True ou False
def checkRede(n1, n2):
	#!!! perguntar pro sor, se todos os ip's vao ter mascara (i.e. se todos vao ter a "/" no ip)
	#se sim -> alterar o código

	if type(n1) == Router.Router or type(n2) == Router.Router:
		return False

	n1 = n1.IP
	n2 = n2.IP

	a = ""
	b = ""
	l = re.split("\.|/", n1)
	mask = int(l[-1])

	for i in range(len(l)-1):
		c = "{0:b}".format(int(l[i]))
		while len(c) != 8:
			c = "0" + c

		a += c

	l = re.split("\.|/", n2)

	for i in range(len(l)-1):
		c = "{0:b}".format(int(l[i]))
		while len(c) != 8:
			c = "0" + c

		b += c

	return a[:mask] == b[:mask]



def parser(file):
    arq = open(file, "r").read()

    n = arq.split('#')[1].split('\n')[1:-1]
    r = arq.split('#')[2].split('\n')[1:-1]
    t = arq.split('#')[3].split('\n')[1:]

    nodes = []
    for elem in n:
        node_info = elem.split(',')
        name = node_info[0]
        MAC = node_info[1]
        IP = node_info[2]
        gateway = node_info[3]
        nodes.append(Node.Node(name, MAC, IP, gateway))

    routers = []
    for elem in r:
        table_info = elem.split(',')
        router_name = table_info[0]
        num_ports = table_info[1]
        IPs = []
        MACs = []
        for i in range(2, len(table_info), 2):
            MACs.append(table_info[i])
            IPs.append(table_info[i+1])
        routers.append(Router.Router(name, router_name, IPs, MACs))


    tables = []
    for elem in t:
        table_info = elem.split(',')
        name = table_info[0]
        net_dest = table_info[1]
        nexthop = table_info[2]
        port = table_info[3]
        tables.append(Router_table.Router_table(name, net_dest, nexthop, port))

    return nodes, routers, tables


def ARP(src, dst):
	#verificar se o src é Node ou Router (pq o atributo IP é diferente em cada classe)
	if type(src) == Router.Router:
		for i in range(len(src.IPs)):
			if src.IPs[i] == (dst.gateway + "/" + dst.IP.split("/")[-1]):
				index = i
				break

		src_aux = dst.gateway #ou tb dst.IPs[index]
		src_MAC = src.MACs[index]

	else:
		src_aux = src.IP.split("/")[0]
		src_MAC = src.MAC

	#verificar se o dst é Node ou Router (pq o atributo IP é diferente em cada classe)
	if type(dst) == Router.Router:
		for i in range(len(dst.IPs)):
			if dst.IPs[i] == (src.gateway + "/" + src.IP.split("/")[-1]):
				index = i
				break

		dst_aux = src.gateway #ou tb dst.IPs[index]
		dst_MAC = dst.MACs[index]

	else:
		dst_aux = dst.IP.split("/")[0]
		dst_MAC = dst.MAC

	imprime(Flag.ARP_req, src_name=src.name, dst_ip=dst_aux, src_ip=src_aux)
	imprime(Flag.ARP_reply, src_name=dst.name, dst_name=src.name, src_ip=dst_aux, mac=dst_MAC)

	#atualiza lista ARP de ambos
	src.lst_ARP.add(dst_MAC)
	dst.lst_ARP.add(src_MAC)

#usar isso quando tiver q procurar a rota de src pra dst (obviamente quando eles sao de redes diferentes)
def search(src, dst, routers):
	#inicialmente vou supor que o gateway "dst" sempre vai estar ligado a uma porta "1"!!!
	rota = []
	#print(dst.gateway + "/" + dst.IP.split("/")[-1])
	for e in routers:
		for i in range(len(e.IPs)):
			if e.IPs[i] == (dst.gateway + "/" + dst.IP.split("/")[-1]):
				a = e
				notA = e.IPs[(i+1)%2] #isso supondo que o tamanho é sempre dois, por cada roteador ter duas portas
				
				if notA == (src.gateway + "/" + dst.IP.split("/")[-1]):
					rota.append(a)
				
				else:
					pass #recursao que talvez quando tiver mais de 1 router vai mudar o hop e pa --> olhar isso aqui entao dps

				break
	
	return rota

def ICMP(src, dst, rota, routers):
	#verifica se sao da mesma rede
	if checkRede(src, dst):
		#checar se precisa do ARP entre src e dst
		if src.MAC not in dst.lst_ARP:
			ARP(src, dst)

	else:
		if type(src) != Router.Router:#gambiarra
			for e in routers:
				for i in range(len(e.IPs)):
					if e.IPs[i] == (dst.gateway + "/" + dst.IP.split("/")[-1]):
						a = e
						break

		else: #outra parte da gambiarra
			a = dst

		#checar se precisa do ARP entre src e seu gateway default
		if type(src) == Router.Router:
			if src.MACs[1] not in a.lst_ARP:
				ARP(src, a)
		
		elif src.MAC not in a.lst_ARP:
			ARP(src, a)

	print("ICMP REQ A->B :)")
	if rota != []:
		ICMP(rota.pop(0), dst, rota, routers)

	print("REPLY ICMP B->A :)")

	