import pygraphviz as pgv
import networkx as nx
import pandas as pd

from lib_base import GraphBenchmark

class PyGraphvizBenchmark(GraphBenchmark):
    def create_graph(self):
        edgelist_df = pd.read_csv(self.edgelist_file, header=None, names=['source', 'target'])
        G = pgv.AGraph(directed=False)
        for _, row in edgelist_df.iterrows():
            G.add_edge(row['source'], row['target'])
        return G

    def perform_pagerank(self, G):
        nx_graph = nx.Graph(G)
        pr_result = nx.pagerank(nx_graph, alpha=0.85)

    def detect_communities(self, G):
        nx_graph = nx.Graph(G)
        community_result = nx.algorithms.community.louvain_communities(nx_graph)
