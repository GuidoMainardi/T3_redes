class Node(object):

    def __init__(self, name, MAC,  IP, gateway):
        self.name = name
        self.MAC = MAC
        self.IP = IP
        self.gateway = gateway


    def imprime(self):
        print(f"Node: {self.name}")
        print(f"MAM: {self.MAC}")
        print(f"IP: {self.IP}")
        print(f"gateway: {self.gateway}\n")
