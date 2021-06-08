class Router_table(object):
    def __init__(self, router_name, net_dest, nexthop, port):
        self.router_name = router_name
        self.net_dest = net_dest
        self.nexthop = nexthop
        self.port = port

    def imprime(self):
        print(f"Router_name: {self.router_name}")
        print(f"net_dest: {self.net_dest}")
        print(f"nexthop: {self.nexthop}")
        print(f"port: {self.port}")