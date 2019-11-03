import argparse
import collections
import pickle
import matplotlib.pyplot as plt
import networkx as nx


class Grapher(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None
        self.link_graph = None

    def __enter__(self):
        self.file = open(self.file_path, 'rb')
        self.link_adj = pickle.load(self.file)
        return self

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

        node_index = {node: i for i, node in enumerate(nodes)}
        link_graph.add_nodes_from(range(0, len(nodes)))

        edges = []
        for nodes_str, weight in edge_weights.items():
            left_node, right_node = nodes_str.split(' ')
            left_node_index = node_index[left_node]
            right_node_index = node_index[right_node]
            edges.append([left_node_index, right_node_index, {"weight": weight}])
        link_graph.add_edges_from(edges)
        return link_graph

    def plot_to_file(self, file_path):
        graph = self.graph()
        plt.figure(figsize=(9, 9))
        nx.draw_networkx(graph)
        plt.savefig(file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pickle_path",
                        help="The path of a pickle file that stores the crawled URLs", type=str, required=True)
    parser.add_argument("-o", "--output-file", help="Output file were the graph will be drawn", type=str, required=True)

    args = parser.parse_args()

    with Grapher(args.pickle_path) as grapher:
        grapher.plot_to_file(args.output_file)


if __name__ == '__main__':
    main()
