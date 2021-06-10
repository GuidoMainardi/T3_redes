class Router(object):

    def __init__(self, name, num_ports, IPs, MACs):
        self.name = name
        self.num_ports = num_ports
        self.IPs = IPs
        self.MACs = MACs
        self.lst_ARP = set()

    def imprime(self):
        print(f"Router: {self.name}")
        print(f"Ports: {self.num_ports}\n")
        for i in range(len(self.IPs)):
            print(f"MAC{i}: {self.MACs[i]}")
            print(f"IP{i}: {self.IPs[i]}")
        print("ARP's conhecidos:", *self.lst_ARP)
        print()