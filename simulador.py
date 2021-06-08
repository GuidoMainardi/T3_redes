def imprime(list):
    for elem in list:
        elem.imprime()
        print()

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

import Node, Router, Router_table
import sys

file = sys.argv[1]
instruction = sys.argv[2]
params = sys.argv[3:]

nodes, routers, tables = parser(file)

imprime(nodes)
imprime(routers)
imprime(tables)