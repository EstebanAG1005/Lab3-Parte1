import heapq

class LinkStateRouting:

    def __init__(self, topology_file, message_file='messages.txt'):
        self.load_topology(topology_file)
        self.message_file = message_file
        self.me = self.pick_node()
        self.visited_nodes = set()

    def load_topology(self, topology_file):
        self.topology = {}
        with open(topology_file, 'r') as f:
            for line in f:
                node, neighbors = line.strip().split(": ")
                self.topology[node] = {}
                for neighbor in neighbors.split(","):
                    n, weight = neighbor.split("-")
                    self.topology[node][n] = int(weight)

    def pick_node(self):
        print(f"Los nodos disponibles son: {list(self.topology.keys())}")
        return input("Elige tu nodo: ")

    def dijkstra(self, start, end):
        shortest_paths = {start: (None, 0)}
        current_node = start
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = self.topology[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node, weight in destinations.items():
                accumulated_weight = weight_to_current_node + weight
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, accumulated_weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if accumulated_weight < current_shortest_weight:
                        shortest_paths[next_node] = (current_node, accumulated_weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return None
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        # Reconstruir el camino desde el destino al origen.
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path.reverse()
        return path


    def deliver_message(self, message, target):
        print("🌟 Preparando mensaje 🌟")
        path = self.dijkstra(self.me, target)
        if path:
            print(f"Ruta óptima encontrada: {' -> '.join(path)}")
            for node in path[1:]:
                print(f"🚀 Enviando mensaje a: {node}")
            with open(self.message_file, 'a') as f:
                f.write(f"{target}:{self.me}:{message}\n")
        else:
            print("No se encontró una ruta al destino.")

    def accept_message(self):
        with open(self.message_file, 'r') as f:
            lines = f.readlines()
        new_lines = []
        received = False
        for line in lines:
            target, sender, message = line.strip().split(":")
            if target == self.me:
                print(f"🎉 Mensaje recibido de {sender}: {message}")
                received = True
            else:
                new_lines.append(line)
        with open(self.message_file, 'w') as f:
            f.writelines(new_lines)
        if not received:
            print(f"No hay mensajes para el nodo {self.me}.")

if __name__ == "__main__":
    routing = LinkStateRouting('topologiaLS.txt')
    options = ["Enviar Mensaje", "Recibir Mensaje", "Cerrar el Programa"]
    while True:
        print("\n📜 Menú:")
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        option = input("🔮 Elige tu opcion: ")

        if option == "1":
            message = input("✒️ Escribe tu mensaje: ")
            target = input("🎯 Indica el destino: ")
            routing.deliver_message(message, target)
        elif option == "2":
            routing.accept_message()
        elif option == "3":
            print("👋 Cerrando el programa. ¡Hasta luego!")
            break
        else:
            print("🚫 Opción no reconocida. Inténtalo de nuevo.")