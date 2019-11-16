from typing import Optional

import igraph

from crawler.crawl import Crawl


class Graph(object):
    def __init__(self, crawl: Crawl, graph: Optional[igraph.Graph] = None):
        self.crawl = crawl
        self.graph = graph

    def build(self):
        links_by_url = self.crawl.links_by_url
        edges = []
        nodes = set(links_by_url.keys())
        for url, links in links_by_url.items():
            nodes |= links
            edges.extend([(url, link) for link in links])
        nodes = list(nodes)
        node_index = {node: index for index, node in enumerate(nodes)}
        g = igraph.Graph(n=len(nodes), directed=True)
        g.vs["name"] = nodes
        g.vs["label"] = g.vs["name"]
        g.add_vertices(len(nodes))
        edges_index = [(node_index[edge[0]], node_index[edge[1]]) for edge in edges]
        g.add_edges(edges_index)
        g.degree(mode="in")
        self.graph = g
        return self.graph

    def __str__(self):
        return '{}' .format(str(self.graph))

    def save_plot(self, file_path, layout='random'):
        layout = self.graph.layout(layout)
        igraph.plot(
            self.graph, file_path,
            layout=layout,
            vertex_label_size=10,
            vertex_label_angle=1,
            vertex_label_dist=0,
            vertex_size=5,
            bbox=(3000, 3000),
            margin=20
        )
