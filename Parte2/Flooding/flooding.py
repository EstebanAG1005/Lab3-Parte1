import logging
import sys
from getpass import getpass
from argparse import ArgumentParser
from aioconsole import ainput
import json
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def menu_options():
    print("\nChoose an option:")
    print("1 - Mandar un mensaje")
    print("2 - Salir")
    option = await ainput("Option: ")
    return option


class Flooding(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.register_plugin("xep_0030")  # Service Discovery
        self.register_plugin("xep_0004")  # Data Forms
        self.register_plugin("xep_0060")  # PubSub
        self.register_plugin("xep_0199")  # XMPP Ping

        self.jid = jid
        self.flag = False
        self.run = False
        self.nodes_visited = []
        self.sent_messages = set()

    def setup_logging(self, level):
        # logging.basicConfig(level=logging.INFO)
        # logging.getLogger("slixmpp").setLevel(level)
        logging.basicConfig(level=logging.ERROR)

    async def start(self, event):

        self.send_presence()
        await self.get_roster()

        with open("user_test.txt") as f:
            self.json_data = json.load(f)

        with open("topo-default.txt") as f:
            self.topology = json.load(f)

        option_cycle = True
        while option_cycle:
            await self.get_roster()
            option = await menu_options()
            if option == "1":
                await self.flood_send()
            elif option == "2":
                option_cycle = False
                self.disconnect()
            else:
                print("Invalid option")

    async def get_input(self, prompt, suffix=""):
        value = await ainput(prompt)
        return value + suffix

    async def flood_send(self):
        user_domain = "@alumchat.xyz"
        user = await self.get_input(
            "Ingrese el usuario al que desea enviar el mensaje (sin @alumchat.xyz): ",
            user_domain,
        )
        message = await self.get_input("Ingrese el mensaje que desea enviar: ")

        msg = {
            "source": self.jid,
            "destination": user,
            "hops": 0,
            "distance": 0,
            "nodes": [],
            "message": message,
        }

        node = self.get_key_by_value(self.jid)
        if node:
            self.process_node(msg, node)
        else:
            print("No hay nodos")

    def get_key_by_value(self, value):
        try:
            return list(self.json_data["config"].keys())[
                list(self.json_data["config"].values()).index(value)
            ]
        except:
            return None

    def process_node(self, msg, node):
        receivers_node = self.topology["config"].get(node)
        if receivers_node:
            print(f"Getting key: {node}")
            print(f"send message to nodes: {receivers_node}")
            msg["hops"] += 1
            msg["nodes"].append(node)
            msg["distance"] += 1
            msg["id"] = id(node)
            if (
                msg["id"] in self.sent_messages
            ):  # Comprobamos si el mensaje ya fue enviado
                print("Mensaje descartado porque es repetido.")
                return
            self.flag = True
            self.nodes_visited.append(node)
            for receiver in receivers_node:
                receiver_jid = self.json_data["config"].get(receiver)
                if receiver_jid:
                    self.send_message(mto=receiver_jid, mbody=str(msg))
            self.sent_messages.add(msg["id"])

    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            msg_f = eval(msg["body"])
            source_node = self.get_key_by_value(msg_f["source"])

            if not self.flag:
                self.nodes_visited.append(source_node)
                self.flag = True
            else:
                self.run = any(node in self.nodes_visited for node in msg_f["nodes"])

            self.display_message(msg_f)

            node = self.get_key_by_value(self.jid)
            if not self.run and node:
                self.process_node(msg_f, node)

    def display_message(self, msg_f):
        if msg_f["destination"] == self.jid:
            print("\nHe llegado a mi destino")
        print("\nMensaje recibido de:", msg_f["source"])
        print("Mensaje para:", msg_f["destination"])
        print("Mensaje:", msg_f["message"])
        print("Saltos:", msg_f["hops"])
        print("Distancia:", msg_f["distance"])
        print("Nodos:", msg_f["nodes"])
        print("\n")
