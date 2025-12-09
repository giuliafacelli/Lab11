import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.id_map = {}

    def build_graph(self, year: int):
        """
        Costruisce il grafo.
        """
        self.G.clear()

        all_rifugi = DAO.get_all_rifugi()

        self.id_map = {}
        for r in all_rifugi:
            self.id_map[r.id_rifugio] = r
            self.G.add_node(r.id_rifugio)

        connessioni = DAO.get_all_connessioni(year)

        for c in connessioni:
            # Controllo di sicurezza: creo l'arco solo se entrambi i nodi esistono
            if c.id_rifugio1 in self.id_map and c.id_rifugio2 in self.id_map:
                self.G.add_edge(c.id_rifugio1, c.id_rifugio2)

        print(f"Grafo creato con {len(self.G.nodes)} nodi e {len(self.G.edges)} archi")

    def get_nodes(self):
        return list(self.G.nodes())

    def get_num_neighbors(self, node):
        return self.G.degree(node)

    def get_num_connected_components(self):
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        reachable = self.get_reachable_recursive(start)
        return reachable

    def get_reachable_recursive(self, start):
        reachable = set()
        visited = set()

        def _ricorsione(current_node):
            visited.add(current_node)
            reachable.add(current_node)

            for neighbor in self.G.neighbors(current_node):
                if neighbor not in visited:
                    _ricorsione(neighbor)

        _ricorsione(start)

        reachable.discard(start)
        return list(reachable)