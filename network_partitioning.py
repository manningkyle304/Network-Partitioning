import collections
import pprint


def nodes_with_distance(graph, n):
    """
    given a distance dictionary, graph, find all nodes
    with a certain distance, n

    Arguments:
    graph -- a dictionary with nodes as keys & distances as values
    n -- an integer

    Returns:
    our_list -- a list of all the nodes with distance n
    """
    our_list = []
    for key, value in graph.items():
        if value == n:
            our_list.append(key)
    return our_list


def bfs(graph, startnode):
    """
    A modified version of BFS that returns the # of
    shortest paths from startnode to each node as well
    as distances.

    Arguments:
    graph -- undirected graph represented as a dictionary
    startnode - node in graph to start the search from

    Returns:
    dist -- a dictionary mapping each node to the node's
     distance from startnode
    npaths -- a dictionary mapping each node to the # of
     shortest paths from startnode
    """
    dist = {}
    npaths = {}

    # Initialize distances and predecessors
    for node in graph:
        dist[node] = float('inf')
    dist[startnode] = 0
    npaths[startnode] = 1
    # Initialize the search queue
    queue = collections.deque([startnode])

    # Loop until all connected nodes have been explored
    while queue:
        curr = queue.popleft()
        for nbr in graph[curr]:
            if dist[nbr] == float('inf'):
                # executes when nbr hasn't been reached before
                dist[nbr] = dist[curr] + 1
                npaths[nbr] = npaths[curr]
                queue.append(nbr)
            elif dist[nbr] == dist[curr] + 1:
                # executes when nbr has been reached before

                # since have reached nbr before, a different
                # node (curr) is also adjacent to nbr, so add the #
                # paths that go through curr to the previous sum
                npaths[nbr] = npaths[nbr] + npaths[curr]
    return dist, npaths


def max_distance(dist_dict):
    """
    Iterates over all dict_values and finds the max distance
    while accounting for situations in which some distances
    are infinity (i.e. for disconnected graphs)

    Arguments:
    dist_dict -- a dictionary mapping keys to integers
    representing distances

    Returns:
    n -- an integer; the maximum value in the dict other than inf
    """
    n = 0

    for distance in dist_dict.values():
        # have to account for infinity (unreachable nodes)
        if distance > n and distance != float('inf'):
            n = distance
    return n


def compute_flow(graph, dist_dict, npaths):
    """
    Computes the flow across all edges of graph using dist
    and npaths from BFS.

    Arguments:
    graph -- undirected graph represented as a dictionary
    dist_dict -- distance dictionary
    npaths -- shortest # paths dictionary

    Returns:
    flow_dict -- a dictionary that maps edges (represented as
    two element tuples with both nodes containing the edge
    as elements) to their respective flow values
    """
    distance = max_distance(dist_dict)

    flow_dict = {}
    while distance > 0:
        # works backwards from the 'max distance' layer

        # find all nodes at 'distance'
        node_list = nodes_with_distance(dist_dict, distance)

        for curr in node_list:
            # iterates over each node curr at 'distance-th' layer

            # local_node_flow is flow calc for curr
            local_node_flow = 1

            for nbr in graph[curr]:
                # this for loop finds the node flow value
                # by iterating over each neighbor of curr

                if dist_dict[nbr] == dist_dict[curr] + 1:
                    # when nbr is on the 'distance+1' layer
                    local_node_flow += flow_dict[frozenset((curr, nbr))]
                    # have to use (curr,nbr) vs. (nbr,curr)
                    # b/c flow_dict set up so keys are
                    # (node w/ 'distance-1', node w/ 'distance')

                elif dist_dict[nbr] == dist_dict[curr]:
                    # when nbr is on the 'distance' layer
                    flow_dict[frozenset((nbr, curr))] = 0

                else:
                    # when nbr is on the 'distance-1' layer
                    weight = npaths[nbr] / float(npaths[curr])
                    flow_dict[frozenset((nbr, curr))] = local_node_flow * weight
        distance -= 1
    return flow_dict


## TESTING ##

if __name__ == '__main__':

    # TEST CASE 1:
    pp = pprint.PrettyPrinter(indent=2)
    fig3_18g = {'A': set(['B', 'C', 'D', 'E']),
                'B': set(['A', 'C', 'F']),
                'C': set(['A', 'B', 'F']),
                'D': set(['A', 'G', 'H']),
                'E': set(['A', 'H']),
                'F': set(['B', 'C', 'I']),
                'G': set(['D', 'I', 'J']),
                'H': set(['D', 'E', 'J']),
                'I': set(['F', 'G', 'K']),
                'J': set(['G', 'H', 'K']),
                'K': set(['I', 'J'])}
    dist, npaths = bfs(fig3_18g, 'A')
    flow1 = compute_flow(fig3_18g, dist, npaths)
    pp.pprint(flow1)

    # TEST CASE 2:
    appendix_graph0 = { 0: set([1, 2]),
                      1: set([0, 3]),
                      2: set([0, 3, 4]),
                      3: set([1, 2, 5]),
                      4: set([2, 5, 6]),
                      5: set([3, 4]),
                      6: set([4]) }
    dist, npaths = bfs(appendix_graph0, 1)
    flow2 = compute_flow(appendix_graph0, dist, npaths)
    pp.pprint(flow2)

    # TEST CASE 3:
    appendix_graph1 = { 0: set([1, 2]),
                      1: set([0, 3]),
                      2: set([0, 3, 4]),
                      3: set([1, 2, 5]),
                      4: set([2, 5, 6]),
                      5: set([3, 4]),
                      6: set([4]) }
    dist, npaths = bfs(appendix_graph1, 2)
    flow3 = compute_flow(appendix_graph1, dist, npaths)
    pp.pprint(flow3)

