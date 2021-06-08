def imprime(list):
    for elem in list:
        elem.imprime()

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
        router_info = elem.split(',')
        name = router_info[0]
        num_ports = router_info[1]
        IPs = []
        MACs = []
        for i in range(2, len(router_info), 2):
            MACs.append(router_info[i])
            IPs.append(router_info[i+1])
        routers.append(Router.Router(name, num_ports, IPs, MACs))


    tables = []
    for elem in t:
        #parser tables
        pass

    return nodes, routers, tables

import Node, Router
import sys

file = sys.argv[1]
instruction = sys.argv[2]
params = sys.argv[3:]

nodes, routers, tables = parser(file)

imprime(nodes)
imprime(routers)