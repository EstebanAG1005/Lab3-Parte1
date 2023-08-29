class UniqueFlooding:

    def __init__(self, topology_file):
        self.load_topology(topology_file)
        self.me = self.pick_node()
        self.neighbors = self.topology.get(self.me, [])
        self.visited_nodes = set()

    def load_topology(self, topology_file):
        self.topology = {}
        with open(topology_file, 'r') as f:
            for line in f:
                node, neighbors = line.strip().split(": ")
                self.topology[node] = neighbors.split(",")

    def pick_node(self):
        print(f"Los nodos disponibles son: {list(self.topology.keys())}")
        return input("Elige tu nodo: ")

    def deliver_message(self, message, target):
        print("🌟 Preparando mensaje 🌟")
        self.visited_nodes.add(self.me)
        self.propagate_message(message, target)

    def propagate_message(self, message, target):
        print(f"🌐 Nodos conectados: {self.neighbors}")
        for neighbor in self.neighbors:
            if neighbor not in self.visited_nodes:
                print(f"🚀 Enviando mensaje a: {neighbor}")
                self.visited_nodes.add(neighbor)

    def accept_message(self, message, sender, target):
        if self.me not in self.visited_nodes:
            self.visited_nodes.add(self.me)
            print(f"🎉 Mensaje recibido de {sender}: {message}")
            self.propagate_message(message, target)

if __name__ == "__main__":
    flooding = UniqueFlooding('topologia.txt')
    options = ["Enviar Mensaje", "Recibir Mensaje", "Cerrar el Programa"]
    while True:
        print("\n📜 Menú:")
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        option = input("🔮 Elige tu destino: ")

        if option == "1":
            message = input("✒️ Escribe tu mensaje: ")
            target = input("🎯 Indica el destino: ")
            flooding.deliver_message(message, target)
        elif option == "2":
            sender = input("💌 ¿De quién es el mensaje recibido? ")
            message = input("📜 ¿Cuál es el mensaje? ")
            target = input("🎯 ¿Cuál es el destino del mensaje? ")
            flooding.accept_message(message, sender, target)
        elif option == "3":
            print("👋 Cerrando el programa. ¡Hasta luego!")
            break
        else:
            print("🚫 Opción no reconocida. Inténtalo de nuevo.")
