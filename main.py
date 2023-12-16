def nxb(f):
    from lib_networkx import NetworkXGraphBenchmark
    NetworkXGraphBenchmark(f).benchmark()

def igb(f):
    from lib_igraph import IGraphBenchmark
    IGraphBenchmark(f).benchmark()

def gtb(f):
    from lib_graph_tool import GraphToolGraphBenchmark
    GraphToolGraphBenchmark(f).benchmark()

def rxb(f):
    from lib_rustworkx import RustworkXGraphBenchmark
    RustworkXGraphBenchmark(f).benchmark()

def gvb(f):
    from lib_graphviz import PyGraphvizBenchmark
    PyGraphvizBenchmark(f).benchmark()

def main():
    import sys

    edgelist_file = sys.argv[1]
    lib = sys.argv[2]
    
    if lib == 'networkx':
        nxb(edgelist_file)
    elif lib == 'igraph':
        igb(edgelist_file)
    elif lib == 'graph-tool':
        gtb(edgelist_file)
    elif lib == 'rustworkx':
        rxb(edgelist_file)
    elif lib == 'pygraphviz':
        gvb(edgelist_file)
    else:
        print("Invalid library. Supported libraries: networkx, igraph, graph-tool, rustworkx, pygraphviz")

if __name__ == "__main__":
    main()
