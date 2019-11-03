import collections
import pickle

import networkx as nx


class Pageranker(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None
        self.link_graph = None

    def __enter__(self):
        self.file = open(self.file_path, 'rb')
        self.link_adj = pickle.load(self.file)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def graph(self):
        link_graph = nx.DiGraph()
        nodes = set()
        edge_weights = collections.defaultdict(int)
        for url, links in self.link_adj.items():
            nodes.add(url)
            nodes |= links
            for link_i in links:
                edge_weights[f"{url} {link_i}"] += 1
        link_graph.add_nodes_from(nodes)

        edges = []
        for nodes_str, weight in edge_weights.items():
            left_node, right_node = nodes_str.split(' ')
            edges.append([left_node, right_node, {"weight": weight}])
        link_graph.add_edges_from(edges)

        return link_graph

    def plot(self):
        pass