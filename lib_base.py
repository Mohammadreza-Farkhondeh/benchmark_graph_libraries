from abc import ABC, abstractmethod
import time
import time
import psutil

class GraphBenchmark(ABC):
    def __init__(self, edgelist_file):
        self.edgelist_file = edgelist_file

    @abstractmethod
    def create_graph(self):
        pass

    @abstractmethod
    def perform_pagerank(self, G):
        pass

    @abstractmethod
    def detect_communities(self, G):
        pass

    def measure_resource_usage(self):
        process = psutil.Process()
        memory_usage = process.memory_info().rss / (1024 ** 1)
        cpu_usage = process.cpu_percent()
        return memory_usage, cpu_usage

    def benchmark(self):
        print(f"Running benchmark for {self.__class__.__name__}...")
        
        start_time = time.time()
        G = self.create_graph()
        loading_time = time.time() - start_time

        start_time = time.time()
        self.perform_pagerank(G)
        pagerank_time = time.time() - start_time

        start_time = time.time()
        self.detect_communities(G)
        community_detection_time = time.time() - start_time

        memory_usage, cpu_usage = self.measure_resource_usage()

        print(f"Loading Time: {loading_time:.4f} seconds")
        print(f"PageRank Time: {pagerank_time:.4f} seconds")
        print(f"Community Detection Time: {community_detection_time:.4f} seconds")
        print(f"Memory Usage: {memory_usage:.2f} KB")
        print(f"CPU Usage: {cpu_usage:.2f}%")
