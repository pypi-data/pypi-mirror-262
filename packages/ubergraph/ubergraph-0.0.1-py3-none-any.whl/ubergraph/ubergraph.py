import pygraphviz as pgv


def ubergraph():
    u = pgv.AGraph(directed=True, strict=False)

    return u


def add_node(u, node):
    u.add_node(node)

    return u


def add_edge(u, edge, node_ins, node_outs, edge_ins, edge_outs):
    u.add_node(str(edge), xlabel=str(edge), shape="point")

    for node_in in node_ins:
        u.add_node(str(node_in))
        u.add_edge(str(edge), str(node_in), arrowhead="inv")

    for node_out in node_outs:
        u.add_node(str(node_out))
        u.add_edge(str(edge), str(node_out))

    for edge_in in edge_ins:
        u.add_node(str(edge_in), xlabel=str(edge_in), shape="point")
        u.add_edge(str(edge), str(edge_in), arrowhead="inv")

    for edge_out in edge_outs:
        u.add_node(str(edge_out), xlabel=str(edge_out), shape="point")
        u.add_edge(str(edge), str(edge_out))

    return u


def get_nodes(u):
    return [node for node in u.nodes() if u.get_node(node).attr["shape"] != "point"]


def get_edges(u):
    return [node for node in u.nodes() if u.get_node(node).attr["shape"] == "point"]

    
def get_from(u, node):
    if node in get_nodes(u):
        return [e1 for (e1, e2) in u.edges() if e2 == node and u.get_edge(e1, e2).attr["arrowhead"] == "inv"] 
    
    elif node in get_edges(u):
        return [e2 for (e1, e2) in u.edges() if e1 == node and e1 != e2 and u.get_edge(e1, e2).attr["arrowhead"] == "inv"] + [node for (e1, e2) in u.edges() if (e1==node and e2==node)] 
    
    else:
        return []


def get_to(u, node):
    if node in get_nodes(u):
        return [e1 for (e1, e2) in u.edges() if e2 == node and u.get_edge(e1, e2).attr["arrowhead"] != "inv"]
    
    elif node in get_edges(u):
        return [e2 for (e1, e2) in u.edges() if e1 == node and e1 != e2 and u.get_edge(e1, e2).attr["arrowhead"] != "inv"] + [node for (e1, e2) in u.edges() if (e1==node and e2==node) ] 
    
    else:
        return []


def get_in_edges(u, node):
    if node in get_nodes(u):
        return get_from(u, node)

    elif node in get_edges(u):
        in_edges_1 = [e1 for (e1, e2) in u.edges() if (e1 in get_edges(u) and e2 == node and e1 != e2 and u.get_edge(e1, e2).attr["arrowhead"] != "inv")]
        circular_edges = [node for (e1, e2) in u.edges() if (e1==node and e2==node)] 
        in_edges_2 = [e2 for (e1, e2) in u.edges() if (e2 in get_edges(u) and e1 == node and e1 != e2 and u.get_edge(e1, e2).attr["arrowhead"] == "inv")]
    
        return in_edges_1 + circular_edges + in_edges_2
    else:
        return []
        

def get_out_edges(u, node):
    if node in get_nodes(u):
        return get_to(u, node)

    elif node in get_edges(u):
        out_edges_1 = [e2 for (e1, e2) in u.edges() if (e2 in get_edges(u) and e1 == node and e1 != e2 and u.get_edge(e1, e2).attr["arrowhead"] != "inv")]
        circular_edges = [node for (e1, e2) in u.edges() if (e1==node and e2==node)] 
        out_edges_2 = [e1 for (e1, e2) in u.edges() if (e1 in get_edges(u) and e2 == node and e1 != e2 and u.get_edge(e1, e2).attr["arrowhead"] == "inv")]
    
        return out_edges_1 + circular_edges + out_edges_2
        
    else:
        return []