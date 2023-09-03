class LinkStateRouting:

    def __init__(self, topology_file):
        self.load_topology(topology_file)
        self.all_routing_tables = {}

    def load_topology(self, topology_file):
        self.topology = {}
        with open(topology_file, 'r') as f:
            for line in f:
                node, neighbors = line.strip().split(": ")
                self.topology[node] = {}
                for neighbor in neighbors.split(","):
                    n, weight = neighbor.split("-")
                    self.topology[node][n] = int(weight)

    def dijkstra(self, start, end):
        shortest_paths = {start: (None, 0)}
        current_node = start
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = self.topology[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node, weight in destinations.items():
                accumulated_weight = weight + weight_to_current_node
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

        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        path.reverse()
        return path

    def generate_routing_table(self, node):
        routing_table = {}
        for target in self.topology:
            if target != node:
                path = self.dijkstra(node, target)
                if path:
                    routing_table[target] = ' -> '.join(path)
        return routing_table

    def simulate(self):
        for node in self.topology:
            routing_table = self.generate_routing_table(node)
            self.all_routing_tables[node] = routing_table

    def run_menu(self):
        while True:
            print("\n--- Menú ---")
            print("1. Ver tablas de enrutamiento")
            print("2. Enviar mensaje de un nodo a otro")
            print("3. Salir")
            choice = input("Elige una opción: ")

            if choice == "1":
                for node, table in self.all_routing_tables.items():
                    print(f"\nTabla de enrutamiento para {node}:")
                    for target, path in table.items():
                        print(f"Ruta óptima a {target}: {path}")
            
            elif choice == "2":
                from_node = input("Nodo de origen: ")
                to_node = input("Nodo de destino: ")
                if from_node in self.all_routing_tables and to_node in self.all_routing_tables[from_node]:
                    print(f"Enviando mensaje de {from_node} a {to_node} a través de la ruta: {self.all_routing_tables[from_node][to_node]}")
                else:
                    print("Ruta no disponible o nodos incorrectos.")
            
            elif choice == "3":
                print("Saliendo...")
                break

            else:
                print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    routing = LinkStateRouting('topologiaLS.txt')
    routing.simulate()
    routing.run_menu()