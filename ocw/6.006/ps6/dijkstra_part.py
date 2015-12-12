def construct_path(self, source):
    path = [source]
    n = source.parent
    while n:
        path.append(n)
        n = n.parent
    return tuple(path)

def dijkstra(self, weight, nodes, source, destination):
    # Node objects are hashable because they are composed of integers
    # and strings: one is a builtin object, and the other is immutable.
    # Since there are no mutable objects, the object is hashable.

    # Initialize. keypair represents the node-d pair to be used in the
    # priority queue, and parent is of course the parent.
    # Adapted from provided solution. By creating these local variables, one no
    # longer needs a dict to provide a mapping between each node and its
    # NodeDistancePair, which is necessary for changing the value of keys
    # during search.
    for node in nodes:
        node.parent = None
        node.keypair = NodeDistancePair(node, None)

    heap = PriorityQueue()
    # By searching from the destination, one no longer needs to reverse the
    # list at the end of of the function if not using a deque. One would assume
    # that as more-often used objects lists are more optimized than deques.
    # However, the difference is likely to be trivial.
    destination.keypair.distance = 0
    heap.insert(destination.keypair) # The queue only needs to store the frontier.

    visitedN = 0

    while True:
        lowest_pair = heap.extract_min()
        visitedN += 1
        # Termination conditions.
        if lowest_pair is None:
            raise Exception("Unexpected error. Queue was emptied but \
            destination node was not found. Was destination node part of \
            all nodes?")
        elif lowest_pair.node == source:
            return self.construct_path(lowest_pair.node), visitedN # Path found. Finish.
        # Otherwise, continue searching.
        # Look at all adjacent nodes of the current lowest-weight node.
        for perimeter_node in lowest_pair.node.adj:
            perimeter_pair = perimeter_node.keypair
            relax_value = lowest_pair.distance + weight(lowest_pair.node,
            perimeter_node)
            # Adapted from solution provided. Genius! Using the
            # None-initialized value for the distance variable to substitute
            # for inifinity. This is done in conjunction with keeping the queue
            # at the lowest size possible - i.e. the current frontier.
            if perimeter_pair.distance is None:
                perimeter_pair.distance = relax_value
                heap.insert(perimeter_pair)
                perimeter_node.parent = lowest_pair.node
            elif relax_value < perimeter_pair.distance:
                perimeter_pair.distance = relax_value
                heap.decrease_key(perimeter_pair)
                perimeter_node.parent = lowest_pair.node
