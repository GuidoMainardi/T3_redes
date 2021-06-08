import re
from enum import Enum
import Node, Router, Router_table

class Flag(Enum):
	ARP_req = 1
	ARP_reply = 2
	ICMP_req = 3
	ICMP_reply = 4
	ICMP_time = 5

def imprime(str, src_ip = 0, src_name = 0, dst_ip = 0, dst_name = 0, ttl = 8, mac = 0):
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
