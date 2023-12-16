import graph_tool.all as gt
import pandas as pd

from lib_base import GraphBenchmark

class GraphToolGraphBenchmark(GraphBenchmark):
    def create_graph(self):
        return gt.load_graph_from_csv(self.edgelist_file)

    def perform_pagerank(self, G):
        gt.pagerank(G)

    def detect_communities(self, G):
        gt.minimize_blockmodel_dl(G).get_blocks().fa.astype(int).tolist()
