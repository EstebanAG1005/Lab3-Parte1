class UniqueFlooding:

    def __init__(self, topology_file):
        self.load_topology(topology_file)
        self.me = self.pick_node()
        self.neighbors = self.topology.get(self.me, [])

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
        print("Iniciando protocolo de envío mágico 🌟")
        self.propagate_message(message, target, [self.me])

    def propagate_message(self, message, target, visited):
        print(f"Revisando conexión mística con: {self.neighbors}")
        for neighbor in self.neighbors:
            if neighbor not in visited:
                print(f"Enviando runas mágicas a: {neighbor}")
                visited.append(neighbor)

    def accept_message(self, message, sender, visited):
        if target == self.me:
            print(f"¡Mensaje recibido desde {sender}! El mensaje es: {message}")
        elif self.me in visited:
            print("Mensaje Recibido. No reenviar.")
        else:
            print(f"Canalizando energías para reenviar a: {self.neighbors}")
            visited.append(self.me)
            self.propagate_message(message, target, visited)


if __name__ == "__main__":
    flooding = UniqueFlooding('topologia.txt')
    option = None
    while option != "3":
        print("\n\n📜 1. Enviar Mensaje")
        print("📜 2. Recibir Mensaje")
        print("📜 3. Cerrar el Programa")
        option = input("🔮 Elige tu destino: ")
        if option == "1":
            message = input("✒️ Inscribir mensaje: ")
            target = input("🎯 Elige el objetivo del mensaje: ")
            flooding.deliver_message(message, target)
        elif option == "2":
            arcane_message = input("✉️ Ingrese el mensaje de la siguiente manera, <objetivo,mensaje,emisor>: ")
            target, message, sender = arcane_message.split(",")
            visited_input = input("🗺 Ingresa el recorrido del mensaje de esta forma <nodo1,nodo2,nodo3> : ")
            visited = visited_input.split(",")
            flooding.accept_message(message, sender, visited)
