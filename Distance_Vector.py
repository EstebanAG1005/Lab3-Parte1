import sys


class DistanceVector:
    def __init__(self, topology_file):
        self.load_topology(topology_file)
        self.me = self.pick_node()
        self.routing_table = {self.me: {"next_hop": self.me, "cost": 0}}
        self.update_table()

    def load_topology(self, topology_file):
        self.topology = {}
        with open(topology_file, "r") as f:
            for line in f:
                node, neighbors = line.strip().split(": ")
                self.topology[node] = {}
                for neighbor in neighbors.split(","):
                    n, cost = neighbor.split(":")
                    self.topology[node][n] = int(cost)

    def pick_node(self):
        print(f"Available nodes: {list(self.topology.keys())}")
        return input("Pick your node: ")

    def update_table(self):
        for neighbor, cost in self.topology[self.me].items():
            if (
                neighbor not in self.routing_table
                or self.routing_table[neighbor]["cost"] > cost
            ):
                self.routing_table[neighbor] = {"next_hop": neighbor, "cost": cost}
        print(f"Updated routing table: {self.routing_table}")

    def share_table(self):
        for neighbor in self.topology[self.me]:
            print(f"Sharing table with {neighbor}")
            # Actual code for updating the neighbor's table would go here

    def send_message(self, destination, message):
        if destination in self.routing_table:
            next_hop = self.routing_table[destination]["next_hop"]
            print(
                f"Sending message to {destination} via {next_hop}. Message: {message}"
            )
        else:
            print(f"Destination {destination} not reachable.")

    def print_routing_table(self):
        print(f"Routing table of {self.me}: {self.routing_table}")


if __name__ == "__main__":
    dv = DistanceVector("topologia_vector.txt")
    option = ""
    while option.upper() != "Q":
        print("\n1. Update Table")
        print("2. Show Table")
        print("3. Send Message")
        print("Q. Quit")
        option = input("Choose an option: ")

        if option == "1":
            dv.update_table()
            dv.share_table()
        elif option == "2":
            dv.print_routing_table()
        elif option == "3":
            destination = input("Enter the destination node: ")
            message = input("Enter the message: ")
            dv.send_message(destination, message)
