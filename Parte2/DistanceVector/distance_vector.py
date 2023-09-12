import logging
import sys
from getpass import getpass
from aioconsole import ainput
import json
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def menu_options():
    print("\n1. Actualizar Tabla")
    print("2. Mostrar Tabla")
    print("3. Enviar Mensaje")
    print("Q. Salir")
    option = await ainput("Selecciona una opcion: ")
    return option


class DistanceVector(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.register_plugin("xep_0030")  # Service Discovery
        self.register_plugin("xep_0004")  # Data Forms
        self.register_plugin("xep_0060")  # PubSub
        self.register_plugin("xep_0199")  # XMPP Ping

        self.load_topology("topo-default.txt")  # Carga de topología
        self.load_names("user_test.txt")  # Carga de nombres

        self.jid = jid
        self.flag = False
        self.run = False

        self.me = self.get_node_from_jid(jid)
        self.routing_table = {self.me: {"next_hop": self.me, "cost": 0}}
        self.update_table()

    def setup_logging(self, level):
        logging.basicConfig(level=level)
        logging.getLogger("slixmpp").setLevel(level)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        option_cycle = True
        while option_cycle:
            await self.get_roster()
            option = await menu_options()
            if option == "1":
                self.update_table()
                self.share_table()  # Comparte la tabla con los vecinos después de actualizarla.
            elif option == "2":
                self.print_routing_table()
            elif option == "3":
                destination = input("Escoge el nodo destinatario (ej: A, B, C): ")
                message = input("Ingresa el mensaje: ")
                self.send_text_message(destination, message)
            elif option.upper() == "Q":
                self.disconnect()

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
            message = {"type": "routing_update", "table": self.routing_table}
            self.send_message(mto=jid, mbody=json.dumps(message))

    def print_routing_table(self):
        print("Tabla de Routing:")
        for dest, info in self.routing_table.items():
            dest_jid = self.names[dest]
            next_hop_jid = self.names[info["next_hop"]]
            print(
                f"Destino: {dest_jid} | Next Hop: {next_hop_jid} | Costo: {info['cost']}"
            )

    def send_text_message(self, destination, message_body=None, original_msg=None):
        if destination in self.routing_table:
            next_hop = self.routing_table[destination]["next_hop"]
            jid = self.names[next_hop]

            # Si original_msg es None, crea un nuevo mensaje
            if original_msg is None:
                message = {
                    "source": self.jid,
                    "destination": self.names[destination],
                    "hops": 1,
                    "distance": self.routing_table[destination]["cost"],
                    "nodes": [self.me],
                    "message": message_body,
                    "id": hash(message_body + self.jid),
                }
            # De lo contrario, usa el mensaje original y actualízalo
            else:
                message = original_msg
                message["hops"] += 1
                message["nodes"].append(self.me)

            self.send_message(mto=jid, mbody=json.dumps(message))
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
            print("Q. Salir")
            option = input("Selecciona una opcion: ")

            if option == "1":
                self.update_table()
                self.share_table()
            elif option == "2":
                self.print_routing_table()
            elif option == "3":
                destination_jid = input("Ingresa el JID del destinatario: ")
                destination = self.get_node_from_jid(destination_jid)
                message = input("Ingresa el mensaje: ")
                self.send_text_message(destination, message)
            elif option.upper() == "Q":
                self.disconnect()

    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            try:
                # Descodificar el mensaje recibido
                decoded_msg = json.loads(msg["body"])

                # Si es una actualización de la tabla de enrutamiento
                if decoded_msg.get("type") == "routing_update":
                    from_node = self.get_node_from_jid(msg["from"].bare)
                    self.receive_table(from_node, decoded_msg["table"])
                    return

                # Comprobar si "destination" y otras claves esperadas están en decoded_msg
                if "destination" not in decoded_msg:
                    print(f"Mensaje no válido de {msg['from'].bare}: {msg['body']}")
                    return

                # Comprobar si este nodo es el destino del mensaje
                if decoded_msg["destination"] == self.jid:
                    print(
                        f"Mensaje recibido de {decoded_msg['source']}: {decoded_msg['message']}"
                    )
                else:
                    to_node = self.get_node_from_jid(decoded_msg["destination"])
                    self.send_text_message(to_node, original_msg=decoded_msg)
            except json.JSONDecodeError:
                print(f"Mensaje recibido de {msg['from'].bare}: {msg['body']}")


if __name__ == "__main__":
    # Necesitas autenticarte con un JID y una contraseña.
    jid = input("Enter your JID: ")
    password = getpass("Enter your password: ")
    dv = DistanceVector(jid, password)
    dv.connect()
    dv.process(forever=True)
