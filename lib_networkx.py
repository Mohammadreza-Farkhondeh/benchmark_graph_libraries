import networkx as nx
import pandas as pd

from lib_base import GraphBenchmark

class NetworkXGraphBenchmark(GraphBenchmark):
    def create_graph(self):
        return nx.from_pandas_edgelist(pd.read_csv(self.edgelist_file, header=None, names=['source', 'target']))

    def perform_pagerank(self, G):
        nx.pagerank(G, alpha=0.85)

    def detect_communities(self, G):
        nx.algorithms.community.louvain_communities(G)
