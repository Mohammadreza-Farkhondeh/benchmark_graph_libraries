from igraph import Graph as IGraph
import pandas as pd
import numpy as np

from lib_base import GraphBenchmark

class IGraphBenchmark(GraphBenchmark):
    def create_graph(self):
        return IGraph().TupleList(
            pd.read_csv(
                self.edgelist_file, header=None,
                sep='\s+',
                names=['source', 'target'],
                dtype=np.int64).iloc[:, [0, 1]].to_records(index=False).tolist())

    def perform_pagerank(self, G):
        G.pagerank()

    def detect_communities(self, G):
        G.community_multilevel()
