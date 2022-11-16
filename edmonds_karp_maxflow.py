# a graph class, based on map, offer a general class for graphs/networks
class graph:
    # graph class initializer, by giving a dictionary,
    # dont give egdes with capacity 0, otherwise the fails happens
    def __init__(self, gdict=None):
        if (gdict == None):
            self.gdict = {}
        else:
            self.gdict = gdict

    
    # debugging use only, return the dict inside the graph
    def get_dict(self):
        return self.gdict


    # get list of keys in the graph
    def key_list(self):
        res = []
        for key in self.gdict.keys():
            res.append(key)
        return res

    
    # get edges coming out from the given vertex
    # return a list of ['vertex', weight] pairs of all edges coming out of the node
    def get_edges(self, vertex):
        return self.gdict.get(vertex)

    
    # get edges node coming out from the given vertex
    def get_edges_node(self, vertex):
        res = []
        all_edges = self.get_edges(vertex)
        if (all_edges == None):
            return []
        for i in range(0, len(all_edges)):
            res.append(all_edges[i][0])
        return res

    
    # check if an edge exist
    def edge_exist(self, start, end):
        if (start not in self.key_list()):
            raise Exception('The given start node not in the graph')
        elif (end not in self.get_edges_node(start)):
            return False
        return True

    
    # get capacity of an edge starting from the start node to the target node
    def get_capacity(self, start_node, target_node):
        edge_weight_pairs = self.get_edges(start_node)
        for e in edge_weight_pairs:
            if (e[0] == target_node):
                return e[1]
        raise Exception('No edges from start node to target node matches the requirements')

    
    # determine max flow through the given path
    # path in form of list from start node to terminal node
    def max_flow_over_path(self, path):
        if (len(path) < 2):
            raise Exception('Invalid path, node less than 2')

        limit = self.get_capacity(path[0], path[1])
        for i in range(0, len(path) - 1):
            curr_weight = self.get_capacity(path[i], path[i+1])
            if (curr_weight < limit):
                limit = curr_weight

        return limit

    
    # update an edge with given capacity
    # handle cases if there is no start or no existing eadge. create new edge if needed
    # (void function)
    def update_edge(self, start, end, capacity):
        if (capacity != 0):
            old_edges_pair = self.get_edges(start)
            try:
                if (self.edge_exist(start, end)):
                    old_value = [end, self.get_capacity(start, end)]
                    old_edges_pair[old_edges_pair.index(old_value)] = [end, capacity]
                else:
                    print('Alert: the edge not here, creating a new one')
                    old_edges_pair.append([end, capacity])
            except Exception as e:
                print('Alert: start node may not be there, creating one')
                print(e)
                old_edges_pair = [[end, capacity]]
            finally:
                self.gdict.update({start: old_edges_pair})
        else:
            old_edges_pair = self.get_edges(start)
            old_value = [end, self.get_capacity(start, end)]
            old_edges_pair.pop(old_edges_pair.index(old_value))
            self.gdict.update({start: old_edges_pair})


    # update augmented path when decide let a maximum flow go through it,
    # the function returns the max flow went through this augmented path during current iteration
    def update_augmented_path(self, augmented_path):
        max_flow = self.max_flow_over_path(augmented_path)
        for i in range(0, len(augmented_path) - 1):
            start = augmented_path[i]
            end = augmented_path[i + 1]
            old_cap = self.get_capacity(start, end)
            new_cap = old_cap - max_flow
            # update the new capacity after we ran a max flow on the route
            self.update_edge(start, end, new_cap)
            # set the residue edge with a capacity of the maxflow
            self.update_edge(end, start, max_flow)
        return max_flow


# generate a list of n repeated elements
def n_node(n, name):
    res = []
    for i in range(0, n):
        res.append(name)
    return res

# convert a path in the form of maps{node: parent} to a list form
def path_to_list(path, source, terminal):
    res = [terminal]
    node = terminal
    while (node != source):
        node = path.get(node)
        res.append(node)

    res.reverse()
    return res


# algorithm to find a shortest path tree
# g: a graph object
def find_shortest_path(g, source, terminal):
    visited = [source]
    all_paths = {}

    # queue stores each level
    # last_node stores the parent of the nodes in queue one by one
    queue = g.get_edges_node(source)

    last_node = n_node(len(queue), source)

    while (len(queue) > 0):
        curr_node = queue.pop()
        curr_parent = last_node.pop()
        if (curr_node not in visited):
            visited.append(curr_node)
            all_paths.update({curr_node:curr_parent})
            if (curr_node == terminal):
                return path_to_list(all_paths, source, terminal)
            curr_child = g.get_edges_node(curr_node)
            queue = curr_child + queue
            last_node = n_node(len(curr_child), curr_node) + last_node

    # didn't find any path to terminal
    return None


# requires distinct node names in graph
def ek_maxflow(g, source, terminal):
    all_augmented_paths = []
    total_max_flow = 0
    curr_sp = find_shortest_path(g, source, terminal)
    while (curr_sp != None):
        all_augmented_paths.append(curr_sp)
        total_max_flow += g.update_augmented_path(curr_sp)
        curr_sp = find_shortest_path(g, source, terminal)
        
    
    return total_max_flow, all_augmented_paths
