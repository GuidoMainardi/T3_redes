import re
from enum import Enum
import Node, Router, Router_table

class Flag(Enum):
	ARP_req = 1
	ARP_reply = 2
	ICMP_req = 3
	ICMP_reply = 4
	ICMP_time = 5

def imprime(str, src_name = 0, src_ip = 0, dst_ip = 0, dst_name = 0, ttl = 0, mac = 0):
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


def getRede(ip):
	a = ""
	l = re.split("\.|/", ip)
	mask = int(l[-1])
	for i in range(len(l)-1):
		c = "{0:b}".format(int(l[i]))
		while len(c) != 8:
			c = "0" + c

		a += c

	d = a[:mask] + "0" * (len(a)-mask)

	#transforma a rede binaria para o formato usado em "topologia.txt"
	return ".".join([str(int(x, 2)) for x in [d[start:start+8] for start in range(0, len(d), 8)]]) + "/" + str(mask)



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
        routers.append(Router.Router(router_name, num_ports, IPs, MACs))

    tables = []
    for elem in t:
        table_info = elem.split(',')
        name = table_info[0]
        net_dest = table_info[1]
        nexthop = table_info[2]
        port = int(table_info[3])
        tables.append(Router_table.Router_table(name, net_dest, nexthop, port))

    return nodes, routers, tables

def getMACbyIP(router, ip):
	for i in range(len(router.IPs)):
		if ip in router.IPs[i]:
			return router.MACs[i]

	print("nao é pra isso acontecer!!")
	return -1


def ARP(src, dst, Rport=None, Rip=None):
	#verificar se ambos sao Router
	if type(src) == Router.Router and type(dst) == Router.Router:
		#pega MAC e IP correto de src
		src_aux = src.IPs[Rport]
		src_MAC = src.MACs[Rport]

		#pega MAC e IP correto de dst
		dst_aux = Rip
		#achar o MAC certo
		dst_MAC = getMACbyIP(dst, Rip)

	#verificar se o src é Node ou Router (pq o atributo IP é diferente em cada classe)
	else:
		if type(src) == Router.Router:
			for i in range(len(src.IPs)):
				if dst.gateway in src.IPs[i]:
					index = i
					break

			src_aux = dst.gateway
			src_MAC = src.MACs[index]

		else:
			src_aux = src.IP.split("/")[0]
			src_MAC = src.MAC

		#verificar se o dst é Node ou Router (pq o atributo IP é diferente em cada classe)
		if type(dst) == Router.Router:
			for i in range(len(dst.IPs)):
				if src.gateway in dst.IPs[i]:
					index = i
					break

			dst_aux = src.gateway
			dst_MAC = dst.MACs[index]

		else:
			dst_aux = dst.IP.split("/")[0]
			dst_MAC = dst.MAC

	imprime(Flag.ARP_req, src_name=src.name, dst_ip=dst_aux.split("/")[0], src_ip=src_aux.split("/")[0])
	imprime(Flag.ARP_reply, src_name=dst.name, dst_name=src.name.split("/")[0], src_ip=dst_aux.split("/")[0], mac=dst_MAC)

	#atualiza lista ARP de ambos
	src.lst_ARP.add(dst_MAC)
	dst.lst_ARP.add(src_MAC)

#funcao auxiliar do search
def getRouter(gateway, routers):
	for router in routers:
		for endereco in router.IPs:
			if gateway in endereco:
				return router
	
	#nao é pra isso acontecer XD
	return -1

#usar isso quando tiver q procurar a rota de src pra dst (obviamente quando eles sao de redes diferentes)
def search(src, dst, routers, tables):
	if type(src) != Router.Router:
		src = getRouter(src.gateway, routers)
		return None, dst.IP, src

	target = getRede(dst.IP)
	router_table = [linha for linha in tables if linha.router_name == src.name]

	for e in router_table:
		if e.net_dest == target:
			#achei
			resp = e.nexthop
			respPort = e.port
			break

		if e.net_dest == "0.0.0.0/0":
			#achei o default
			resp = e.nexthop
			respPort = e.port

	if resp == "0.0.0.0":
		#cheguei no nodo
		return respPort, resp, dst

	return respPort, resp, getRouter(resp, routers)
	

termina = 0
def ICMP(src, dst, routers, tables, sender, n, reverse, time_ip=None):
	global termina

	#verifica se deu time exceed na rede
	if n == 0:
		#verificar se agora o "sender" é um roteador para, caso seja, passar um IP valido (se não ele vai passar uma lista de IPs na hora de imprimir)
		if type(src) == Router.Router:
			#pegando o IP certo
			porta, dstIP, prox_passo = search(src, sender, routers, tables)

			ICMP(src, sender, routers, tables, src, 8, 2, time_ip=src.IPs[porta])

		else:
			ICMP(src, sender, routers, tables, src, 8, 2)

	#verifica se sao da mesma rede
	mesma_rede = checkRede(src, dst)
	if mesma_rede:
		#se sim, entao ambos sao Node
		#checar se precisa do ARP entre src e dst
		prox_passo = dst
		if src.MAC not in dst.lst_ARP:
			ARP(src, dst)
		
		if reverse == 1:
			imprime(Flag.ICMP_reply, src_name=src.name, dst_name=dst.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

		elif reverse == 0:
			imprime(Flag.ICMP_req, src_name=src.name, dst_name=dst.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

		elif reverse == 2:
			if time_ip == None:
				imprime(Flag.ICMP_time, src_name=src.name, dst_name=dst.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

			else:
				imprime(Flag.ICMP_time, src_name=src.name, dst_name=dst.name, src_ip=time_ip.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

	else:
		porta, dstIP, prox_passo = search(src, dst, routers, tables)
		#senao -> verificar se precisa de ARP entre src e seu gatemay (Router)
		if type(src) == Router.Router:
			if type(prox_passo) == Router.Router:
				#de roteador pra roteador
				if getMACbyIP(prox_passo, dstIP) not in src.lst_ARP:
					ARP(src, prox_passo, Rport=porta, Rip=dstIP)
				
				if reverse == 1:
					imprime(Flag.ICMP_reply, src_name=src.name, dst_name=prox_passo.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

				elif reverse == 0:
					imprime(Flag.ICMP_req, src_name=src.name, dst_name=prox_passo.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

				elif reverse == 2:
					if time_ip == None:
						imprime(Flag.ICMP_time, src_name=src.name, dst_name=prox_passo.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

					else:
						imprime(Flag.ICMP_time, src_name=src.name, dst_name=prox_passo.name, src_ip=time_ip.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

			else:
				#de roteador pra nodo
				if prox_passo.MAC not in src.lst_ARP:
					ARP(src, prox_passo)

				if reverse == 1:
					imprime(Flag.ICMP_reply, src_name=src.name, dst_name=dst.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

				elif reverse == 0:
					imprime(Flag.ICMP_req, src_name=src.name, dst_name=dst.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

				elif reverse == 2:
					if time_ip == None:
						imprime(Flag.ICMP_time, src_name=src.name, dst_name=dst.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

					else:
						imprime(Flag.ICMP_time, src_name=src.name, dst_name=dst.name, src_ip=time_ip.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

		else:
			#de nodo pra roteador
			a = getRouter(src.gateway, routers)
			if src.MAC not in a.lst_ARP:
				ARP(src, a)

			if reverse == 1:
				imprime(Flag.ICMP_reply, src_name=src.name, dst_name=prox_passo.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

			elif reverse == 0:
				imprime(Flag.ICMP_req, src_name=src.name, dst_name=prox_passo.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

			elif reverse == 2:
				if time_ip == None:
					imprime(Flag.ICMP_time, src_name=src.name, dst_name=prox_passo.name, src_ip=sender.IP.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

				else:
					imprime(Flag.ICMP_time, src_name=src.name, dst_name=prox_passo.name, src_ip=time_ip.split("/")[0], dst_ip=dst.IP.split("/")[0], ttl=n)

	if not mesma_rede and prox_passo != dst:
		ICMP(prox_passo, dst, routers, tables, sender, n-1, reverse, time_ip=time_ip)

	elif reverse == 0:
		if termina == 1:
			exit()
		
		else:
			termina = 1
			ICMP(prox_passo, sender, routers, tables, dst, 8, 1)

	elif reverse == 2:
		exit()


	