import pandas as pd
import pytest
import networkx as nx
import igraph
import rustworkx
import graph_tool.all as gt
import pygraphviz as pgv


@pytest.fixture
def edgelist_df():
    file_path = 'congress.edgelist'
    return pd.read_csv(file_path, sep='\s+', header=None, names=['source', 'target', 'details'])

@pytest.mark.parametrize('library', ['networkx', 'igraph', 'rustgraph', 'graphtools', 'pygraphviz'])
def test_conversion_and_analysis(benchmark, edgelist_df, library):
    graph = None
    def load_edgelist_df():
        return edgelist_df.copy()

    def convert_df_to_graph(df):
        print(df['source'][1])
        if library == 'networkx':
            graph = nx.from_pandas_edgelist(df)
        elif library == 'igraph':
            graph = igraph.Graph.TupleList(df.itertuples(index=False), directed=False)
        elif library == 'rustgraph':
            G = rustworkx.PyGraph()
            graph = G.add_edges_from_no_data(df.iloc[:, [0, 1]].to_records(index=False).tolist())
        elif library == 'graphtools':
            G = gt.Graph(directed=False)
            G.add_edge_list(df.iloc[:, [0, 1]].to_records(index=False).tolist())
            graph = G
        elif library == 'pygraphviz':
            G = pgv.AGraph(directed=False)
            for _, row in df.iterrows():
                G.add_edge(row['source'], row['target'])
            graph = G
        else:
            raise ValueError(f"Unsupported library: {library}")

    def compute_pagerank(G):
        if isinstance(G, nx.Graph):
            return nx.pagerank(G, alpha=0.85)
        elif isinstance(G, igraph.Graph):
            return G.pagerank()
        elif isinstance(G, rustworkx.PyGraph):
            return rustworkx.pagerank(G)
        elif isinstance(G, gt.Graph):
            pr = gt.pagerank(G)
            return {v: pr[v] for v in G.iter_vertices()}
        elif isinstance(G, pgv.AGraph):
            return nx.pagerank(nx.Graph(G), alpha=0.85)
        else:
            raise ValueError(f"Unsupported library: {type(G).__name__}")

    def detect_communities(G):
        if isinstance(G, nx.Graph):
            return nx.algorithms.community.louvain_communities(G)
        elif isinstance(G, igraph.Graph):
            return G.community_multilevel()
        elif isinstance(G, rustworkx.PyGraph):
            return rustworkx.connected_components(G)
        elif isinstance(G, gt.Graph):
            state = gt.minimize_blockmodel_dl(G)
            return state.get_blocks().fa.astype(int).tolist()
        elif isinstance(G, pgv.AGraph):
            return nx.algorithms.community.louvain_communities(nx.Graph(G))
        else:
            raise ValueError(f"Unsupported library: {type(G).__name__}")

    def compute_betweeness(G):
        if isinstance(G, nx.Graph):
            return nx.pagerank(G, alpha=0.85)
        elif isinstance(G, igraph.Graph):
            return G.community_edge_betweenness()
        elif isinstance(G, rustworkx.PyGraph):
            return rustworkx.betweenness_centrality(G)
        elif isinstance(G, gt.Graph):
            pr = gt.betweenness(G)
            return {v: pr[v] for v in G.iter_vertices()}
        elif isinstance(G, pgv.AGraph):
            return nx.pagerank(nx.Graph(G), alpha=0.85)
        else:
            raise ValueError(f"Unsupported library: {type(G).__name__}")

    benchmark(convert_df_to_graph, load_edgelist_df())
    # benchmark.pedantic(convert_df_to_graph, args=(load_edgelist_df(),), rounds=5, iterations=10)
    
    # benchmark.pedantic(compute_pagerank, args=(graph,), rounds=5, iterations=10)

    # benchmark.pedantic(detect_communities, args=(graph,), rounds=5, iterations=10)

    # benchmark.pedantic(compute_betweeness, args=(graph,), rounds=5, iterations=10)
