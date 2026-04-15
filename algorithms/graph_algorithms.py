"""
Advanced Algorithms - Graph Algorithms
"""

from collections import deque, defaultdict
from typing import List, Dict, Set, Tuple, Optional
import heapq


class Graph:
    """Graph class implementing various graph algorithms"""
    
    def __init__(self):
        self.adjacency_list = defaultdict(list)
    
    def add_edge(self, u: str, v: str, weight: int = 1):
        """Add an edge to the graph"""
        self.adjacency_list[u].append((v, weight))
        # For undirected graph, uncomment the following line:
        # self.adjacency_list[v].append((u, weight))
    
    def bfs(self, start: str, target: Optional[str] = None) -> Dict:
        """
        Breadth-First Search
        Returns shortest path and distances from start node
        """
        visited = set()
        queue = deque([(start, [start])])
        distances = {start: 0}
        paths = {}
        
        while queue:
            node, path = queue.popleft()
            
            if node not in visited:
                visited.add(node)
                paths[node] = path
                
                if node == target:
                    return {'path': path, 'distance': distances[node]}
                
                for neighbor, _ in self.adjacency_list[node]:
                    if neighbor not in visited:
                        distances[neighbor] = distances[node] + 1
                        queue.append((neighbor, path + [neighbor]))
        
        return {'visited': visited, 'distances': distances, 'paths': paths}
    
    def dfs(self, start: str, visited: Optional[Set] = None) -> List:
        """
        Depth-First Search
        Returns all nodes reachable from start
        """
        if visited is None:
            visited = set()
        
        visited.add(start)
        result = [start]
        
        for neighbor, _ in self.adjacency_list[start]:
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))
        
        return result
    
    def dfs_iterative(self, start: str) -> List:
        """Iterative Depth-First Search"""
        visited = set()
        stack = [start]
        result = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                
                # Add neighbors in reverse order to maintain order
                for neighbor, _ in reversed(self.adjacency_list[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dijkstra(self, start: str) -> Dict:
        """
        Dijkstra's Algorithm - Shortest path from start to all nodes
        """
        distances = {node: float('infinity') for node in self.adjacency_list}
        distances[start] = 0
        previous = {}
        priority_queue = [(0, start)]
        visited = set()
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            for neighbor, weight in self.adjacency_list[current_node]:
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return {'distances': distances, 'previous': previous}
    
    def shortest_path(self, start: str, end: str) -> Tuple[int, List]:
        """Find shortest path between two nodes using Dijkstra"""
        result = self.dijkstra(start)
        distances = result['distances']
        previous = result['previous']
        
        if distances[end] == float('infinity'):
            return float('infinity'), []
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        return distances[end], path[::-1]
    
    def has_cycle(self) -> bool:
        """Detect if graph has a cycle (for directed graph)"""
        visited = set()
        recursion_stack = set()
        
        def dfs_cycle(node):
            visited.add(node)
            recursion_stack.add(node)
            
            for neighbor, _ in self.adjacency_list[node]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
            
            recursion_stack.remove(node)
            return False
        
        for node in self.adjacency_list:
            if node not in visited:
                if dfs_cycle(node):
                    return True
        
        return False
    
    def topological_sort(self) -> List:
        """Topological sort using DFS (for DAG)"""
        visited = set()
        result = []
        
        def dfs_topological(node):
            visited.add(node)
            for neighbor, _ in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_topological(neighbor)
            result.append(node)
        
        for node in self.adjacency_list:
            if node not in visited:
                dfs_topological(node)
        
        return result[::-1]  # Reverse to get topological order
    
    def is_connected(self) -> bool:
        """Check if graph is connected"""
        if not self.adjacency_list:
            return True
        
        start_node = next(iter(self.adjacency_list))
        visited = set(self.dfs(start_node))
        
        return len(visited) == len(self.adjacency_list)
    
    def find_components(self) -> List[List]:
        """Find connected components in the graph"""
        visited = set()
        components = []
        
        for node in self.adjacency_list:
            if node not in visited:
                component = self.dfs(node, visited)
                components.append(component)
        
        return components


def create_sample_graph():
    """Create a sample graph for demonstrations"""
    graph = Graph()
    
    # Add edges (node1, node2, weight)
    graph.add_edge('A', 'B', 4)
    graph.add_edge('A', 'C', 2)
    graph.add_edge('B', 'C', 5)
    graph.add_edge('B', 'D', 10)
    graph.add_edge('C', 'E', 3)
    graph.add_edge('E', 'D', 4)
    graph.add_edge('D', 'F', 11)
    
    return graph


def create_dag():
    """Create a Directed Acyclic Graph for topological sort"""
    graph = Graph()
    
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('C', 'D')
    graph.add_edge('D', 'E')
    
    return graph


def create_cyclic_graph():
    """Create a graph with a cycle"""
    graph = Graph()
    
    graph.add_edge('A', 'B')
    graph.add_edge('B', 'C')
    graph.add_edge('C', 'A')  # Creates a cycle
    graph.add_edge('C', 'D')
    
    return graph


def main():
    """Main function to demonstrate graph algorithms"""
    print("Graph Algorithms Examples")
    print("=" * 50)
    
    # Create sample graph
    graph = create_sample_graph()
    
    print("\n1. Graph Structure:")
    print("   Nodes:", list(graph.adjacency_list.keys()))
    print("   Edges:")
    for node, edges in graph.adjacency_list.items():
        for edge in edges:
            print(f"     {node} -> {edge[0]} (weight: {edge[1]})")
    
    # BFS
    print("\n2. Breadth-First Search:")
    bfs_result = graph.bfs('A', 'D')
    print(f"   Shortest path from A to D: {bfs_result['path']}")
    print(f"   Distance: {bfs_result['distance']}")
    
    print("\n   BFS from A (all nodes):")
    bfs_all = graph.bfs('A')
    print(f"   Visited order: {list(bfs_all['visited'])}")
    print(f"   Distances: {bfs_all['distances']}")
    
    # DFS
    print("\n3. Depth-First Search:")
    dfs_result = graph.dfs('A')
    print(f"   DFS from A (recursive): {dfs_result}")
    
    dfs_iterative = graph.dfs_iterative('A')
    print(f"   DFS from A (iterative): {dfs_iterative}")
    
    # Dijkstra's Algorithm
    print("\n4. Dijkstra's Shortest Path Algorithm:")
    dijkstra_result = graph.dijkstra('A')
    print("   Shortest distances from A:")
    for node, distance in dijkstra_result['distances'].items():
        print(f"     A -> {node}: {distance}")
    
    print("\n   Shortest path from A to F:")
    distance, path = graph.shortest_path('A', 'F')
    print(f"     Distance: {distance}")
    print(f"     Path: {path}")
    
    # Cycle Detection
    print("\n5. Cycle Detection:")
    cyclic_graph = create_cyclic_graph()
    print(f"   Sample graph has cycle: {cyclic_graph.has_cycle()}")
    print(f"   DAG has cycle: {create_dag().has_cycle()}")
    
    # Topological Sort
    print("\n6. Topological Sort:")
    dag = create_dag()
    topological_order = dag.topological_sort()
    print(f"   Topological order: {topological_order}")
    
    # Connectivity
    print("\n7. Graph Connectivity:")
    print(f"   Is sample graph connected: {graph.is_connected()}")
    
    # Connected Components
    print("\n8. Connected Components:")
    components = graph.find_components()
    print(f"   Number of components: {len(components)}")
    for i, component in enumerate(components):
        print(f"     Component {i + 1}: {component}")
    
    print("\n" + "=" * 50)
    print("Graph Algorithms Key Concepts:")
    print("✓ BFS explores nodes level by level (shortest path)")
    print("✓ DFS explores as deep as possible before backtracking")
    print("✓ Dijkstra finds shortest paths in weighted graphs")
    print("✓ Topological sort orders nodes in a DAG")
    print("✓ Cycle detection prevents infinite loops")
    print("✓ Connected components identify graph structure")


if __name__ == "__main__":
    main()