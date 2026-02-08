"""
# ============================================
# STUDENT IMPLEMENTATION FILE - TASK 2
# You may edit this file.
# Do NOT modify function signatures.
# ============================================

TASK 2: Minimum Spanning Trees

Implement two functions:
1. MST(graph) - Find a minimum spanning tree
2. second_best_ST(graph) - Find the second-best spanning tree

You may implement Union-Find in this file or use the example from examples/union_find_example.py
"""


from graph import Graph
from examples.union_find_example import UnionFind
from typing import List, Tuple, Optional


def MST(graph: Graph) -> List[Tuple[str, str, float]]:
    """
    Find a minimum spanning tree.
    
    Args:
        graph: An undirected, weighted graph
        
    Returns:
        A list of edges (u, v, weight) that form the MST.
        
    Raises:
        ValueError: If graph is directed
        
    Note:
        If the graph is disconnected, returns a minimum spanning forest.
        You may use Kruskal's, Prim's, or any other MST algorithm.
    """
    # TODO: Implement MST algorithm (Kruskal's recommended)
    # Hint: Sort edges by weight, use Union-Find to detect cycles
    if graph.directed:
        raise ValueError(f"Graph is directed")
    
    A: List[Tuple[str, str, float]] = []
    uf = UnionFind(graph.vertices())

    # sort by weight
    edges_sorted = sorted(graph.edges(), key=lambda edge: edge[2])
    
    for u, v, weight in edges_sorted:
        if uf.find(u) != uf.find(v):
            A.append((u, v, weight))
            uf.union(u, v)

    # Not exactly sure what a minimum spanning forest specifically
    # is, but it returns the MST of each disconnected graph
    # correctly according my tests.
    return A


def second_best_ST(graph: Graph) -> Optional[List[Tuple[str, str, float]]]:
    """
    Find the second-best spanning tree.
    
    The second-best spanning tree is a spanning tree with weight > MST weight,
    but the smallest weight possible among all spanning trees.
    
    Args:
        graph: An undirected, weighted graph
        
    Returns:
        A list of edges forming the second-best spanning tree,
        or None if no second-best spanning tree exists.
        
    Raises:
        ValueError: If graph is directed
        
    Hint:
        One MST algorithm works as follows:
        1. Find the MST
        2. For each edge NOT in MST, try adding it (creates a cycle)
        3. Remove the heaviest edge in that cycle (other than the added edge)
        4. This gives a candidate spanning tree.
        5. Return the candidate with minimum weight.

        NOTE: This is just a hint, you may implement it differently.
        NOTE: Naive implementations may be too slow for large graphs.
    """
    # TODO: Implement second-best spanning tree algorithm
    if graph.directed:
        raise ValueError(f"Graph is directed")
    
    mst = MST(graph)

    # E \ MST(edges)
    E_not_mst: List[Tuple[str, str, float]] = list(set(graph.edges()) - set(mst))

    # For any MST edge (u, v) find the edge 
    # (u, *) || (*, u) || (*, v) || (v, *) in E_not_mst
    # with the smallest weight difference in regard to (u, v)

    # Initialize with first elem. Chosen arbitrarily
    min_diff_edge = ()
    min_diff = -1

    # Initialize a new graph. It will be graph \ min_diff_edge
    new_graph = Graph(directed=False, weighted=True)

    for u, v, w1 in mst:
        for x, y, w2 in E_not_mst:
            new_graph.add_edge(x, y, w2)
            if (u in (x, y) or v in (x, y)) and abs(w1-w2) > 0:
                
                if abs(w1-w2) < min_diff or min_diff == -1:
                    min_diff = abs(w1-w2)
                    min_diff_edge = (u, v, w1)
        
    # No second spanning tree
    if min_diff == -1:
        return None
    
    # Remove the edge with the smallest weight difference compared 
    # to its second lightest edge
    mst = list(set(mst) - set([min_diff_edge]))
    for u, v, w in mst:
        new_graph.add_edge(u, v, w)
    
    second_st = MST(new_graph)

    return second_st