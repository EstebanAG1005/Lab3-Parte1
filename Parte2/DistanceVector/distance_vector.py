import sys
import json
import slixmpp


class DistanceVector(slixmpp.ClientXMPP):
    def __init__(self, jid, password, topology_file, names_file):
        super(DistanceVector, self).__init__(jid, password)

        self.load_names(names_file)
        self.load_topology(topology_file)
        self.me = self.get_node_from_jid(jid)
        self.routing_table = {self.me: {"next_hop": self.me, "cost": 0}}
        self.update_table()

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def load_topology(self, topology_file):
        with open(topology_file, "r") as f:
            data = json.load(f)
            self.topology = {
                k: {i[0]: i[1] for i in v} for k, v in data["config"].items()
            }

    def load_names(self, names_file):
        with open(names_file, "r") as f:
            self.names = json.load(f)["config"]

    def get_node_from_jid(self, jid):
        for node, node_jid in self.names.items():
            if node_jid == jid:
                return node
        raise ValueError("Invalid JID")

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
            jid = self.names[neighbor]
            self.send_message(mto=jid, mbody=json.dumps(self.routing_table))

    def send_text_message(self, destination, message):
        if destination in self.routing_table:
            next_hop = self.routing_table[destination]["next_hop"]
            jid = self.names[next_hop]
            self.send_message(mto=jid, mbody=message)
        else:
            print(f"Destino {destination} no alcanzable.")

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        # Menu para las acciones del usuario.
        option = ""
        while option.upper() != "Q":
            print("\n1. Actualizar Tabla")
            print("2. Mostrar Tabla")
            print("3. Enviar Mensaje")
            print("4. Simular Recepcion de Tabla")
            print("Q. Salir")
            option = input("Selecciona una opcion: ")

            if option == "1":
                self.update_table()
                self.share_table()
            elif option == "2":
                self.print_routing_table()
            elif option == "3":
                destination = input("Escoge el nodo destinatario (ej: A, B, C): ")
                message = input("Ingresa el mensaje: ")
                self.send_text_message(destination, message)
            elif option == "4":
                from_node = input("Simulando recepcion de tabla de cual nodo? ")
                simulated_received_table = self.get_routing_table_for_node(from_node)
                self.receive_table(from_node, simulated_received_table)
            elif option.upper() == "Q":
                self.disconnect()

    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            try:
                received_table = json.loads(msg["body"])
                from_node = self.get_node_from_jid(msg["from"].bare)
                self.receive_table(from_node, received_table)
            except json.JSONDecodeError:
                print(f"Mensaje recibido de {msg['from'].bare}: {msg['body']}")


if __name__ == "__main__":
    # Necesitas autenticarte con un JID y una contraseña.
    jid = input("Enter your JID: ")
    password = input("Enter your password: ")
    dv = DistanceVector(jid, password, "topo-default.txt", "user_test.txt")
    dv.connect()
    dv.process(forever=True)
