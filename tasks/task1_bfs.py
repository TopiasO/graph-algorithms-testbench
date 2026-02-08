"""
# ============================================
# STUDENT IMPLEMENTATION FILE - TASK 1
# You may edit this file.
# Do NOT modify function signatures.
# ============================================

TASK 1: Shortest Paths with Maximal Blue Nodes

Given a graph where some vertices are marked as "blue", find a shortest path
from s to t that goes through the maximum number of blue vertices.

In other words:
1. Find all shortest paths from s to t (paths with minimum number of edges)
2. Among those shortest paths, return the maximum number of blue vertices
   that can be visited on any single shortest path

The graph will have a "blue" attribute on vertices (a set of vertex names).
"""

from graph import Graph
from typing import Set, Tuple, Dict, List
from collections import deque


def max_blue_path(graph: Graph, s: str, t: str) -> int:
    """
    Find the maximum number of blue vertices on any shortest path from s to t.
    
    Args:
        graph: The input graph with a 'blue' attribute (set of blue vertex names)
        s: Source vertex
        t: Target vertex
        
    Returns:
        The maximum number of blue vertices that can be visited on any 
        shortest path from s to t. Returns 0 if no path exists.
        
    Raises:
        KeyError: If source or target vertex does not exist in graph
        
    Note:
        - Blue vertices are stored in graph.blue (a set)
        - You need to find shortest paths first, then count blue vertices
        - Only consider paths with minimum edge count (shortest paths)
    """
    # TODO: Implement maximal blue nodes on shortest paths
    # Hints:
    # 1. Use BFS to find distance from s to all vertices
    # 2. Use BFS from t to find distance to all vertices (reverse direction)
    # 3. A vertex v is on a shortest path if dist[s][v] + dist[v][t] == dist[s][t]
    # 4. Use dynamic programming or BFS to track max blue count along paths
    
    blues = 0

    if s not in graph.vertices():
        raise KeyError(f"Start vertex {s} not found in graph")
    elif t not in graph.vertices():
        raise KeyError(f"Target vertex {t} not found in graph")
    
    if s in graph.blue:
        blues += 1

    if s == t:
        return blues
    
    # Dict of visited vertices. List[0] = length of the path there, List[1] = the amount of blue vertices
    # on said path.
    visited: Dict[str, List[int]] = {}
    
    queue = deque([s])

    # Place the start vertex in visited
    visited[s] = [0, blues]
    

# Regular bfs, but it keeps track of the length of the path to a certain vertex and the amount of 
# blues on said path. Updates the amount of blues if a path that is of the same length to particular
# vertex is found that has more blue vertices on it.
    while queue:
        vertex = queue.popleft()
        # Get length and blue from visited
        length = visited[vertex][0]
        blue = visited[vertex][1]

        # Due to the nature of bfs. If length == the saved len(s to t) then
        # finding paths of len(s to t) is no longer possible.
        if t in visited and length == visited[t][0]:
            break

        for neighbor in graph.neighbors(vertex):
            new_length = length + 1
            new_blue = blue
            if neighbor in graph.blue:
                new_blue = blue +1
            if neighbor not in visited:
                visited[neighbor] = [new_length, new_blue]
                queue.append(neighbor)

            # If the neighbor vertex has already been visited and this new path
            # is as short as the previous one -> Compare the amount of blue
            # vertices.
            elif neighbor in visited and visited[neighbor][0] == new_length:
                if visited[neighbor][1] < new_blue:
                    visited[neighbor][1] = new_blue

    # t is in visited only if there is a path from s to t
    if t in visited:
        return visited[t][1]
    else:
        return 0
    
