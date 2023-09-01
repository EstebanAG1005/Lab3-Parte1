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
        print(f"Los nodos disponibles son: {list(self.topology.keys())}")
        return input("Elige tu nodo: ")

    def update_table(self):
        for neighbor, cost in self.topology[self.me].items():
            if (
                neighbor not in self.routing_table
                or self.routing_table[neighbor]["cost"] > cost
            ):
                self.routing_table[neighbor] = {"next_hop": neighbor, "cost": cost}
        print(f"Tabla de routing actualizada: {self.routing_table}")

    def receive_table(self, from_node, received_table):
        for destination, info in received_table.items():
            new_cost = (
                self.topology[self.me].get(from_node, float("inf")) + info["cost"]
            )
            if (
                destination not in self.routing_table
                or self.routing_table[destination]["cost"] > new_cost
            ):
                self.routing_table[destination] = {
                    "next_hop": from_node,
                    "cost": new_cost,
                }
        print(
            f"Tabla de routing actualizada despues de recibir tabla de {from_node}: {self.routing_table}"
        )

    def share_table(self):
        for neighbor in self.topology[self.me]:
            print(f"Enviado tabla a:  {neighbor}")
            # Actual code for updating the neighbor's table would go here

    def send_message(self, destination, message):
        if destination in self.routing_table:
            next_hop = self.routing_table[destination]["next_hop"]
            print(
                f"Enviando mensaje a {destination} via {next_hop}. Mensaje: {message}"
            )
        else:
            print(f"Destino {destination} no alcanzable.")

    def print_routing_table(self):
        print(f"Tabla de routing de {self.me}: {self.routing_table}")

    def get_routing_table_for_node(self, node):
        """Generando tabla de routing para el nodo escogido."""
        routing_table = {node: {"next_hop": node, "cost": 0}}
        for neighbor, cost in self.topology[node].items():
            routing_table[neighbor] = {"next_hop": neighbor, "cost": cost}
        return routing_table


if __name__ == "__main__":
    dv = DistanceVector("topologia_vector.txt")
    option = ""
    while option.upper() != "Q":
        print("\n1. Actualizar Tabla")
        print("2. Mostrar Tabla")
        print("3. Enviar Mensaje")
        print("4. Simular Recepcion de Tabla")
        print("Q. Salir")
        option = input("Selecciona una opcion: ")

        if option == "1":
            dv.update_table()
            dv.share_table()
        elif option == "2":
            dv.print_routing_table()
        elif option == "3":
            destination = input("Escoge el nodo destinatario: ")
            message = input("Ingresa el mensaje: ")
            dv.send_message(destination, message)
        elif option == "4":
            from_node = input("Simulando recepcion de tabla de cual nodo? ")
            simulated_received_table = dv.get_routing_table_for_node(from_node)
            dv.receive_table(from_node, simulated_received_table)
