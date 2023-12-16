import rustworkx
import pandas as pd

from lib_base import GraphBenchmark

class RustworkXGraphBenchmark(GraphBenchmark):
    def create_graph(self):
        g = rustworkx.PyGraph()
        df = pd.read_csv(
                self.edgelist_file, sep='\s+', header=None, names=['source', 'target']).to_records(index=False).tolist()
        nodes = list(set(node for edge in df for node in edge))

        g.add_nodes_from(nodes)

        g.add_edges_from_no_data(df)

        return g
    
    def perform_pagerank(self, G):
        rustworkx.pagerank(G.to_directed())

    def detect_communities(self, G):
        rustworkx.connected_components(G)
