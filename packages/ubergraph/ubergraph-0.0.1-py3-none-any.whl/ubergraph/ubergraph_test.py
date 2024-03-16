import ubergraph

if __name__ == "__main__":
    u = ubergraph.ubergraph()
    u = ubergraph.add_node(u, "node1")
    u = ubergraph.add_edge(u, "edge1", ["node1"], ["node2", "node3"], ["edge2"], [])
    u = ubergraph.add_edge(u, "edge2", ["node1"], ["node2"], ["edge2"], ["edge2", "edge2"])#, [])

    print(u)
    print(ubergraph.get_nodes(u))
    print(ubergraph.get_edges(u))

    print("nodes:", u.nodes())
    print("edges:", u.edges())

    print("node1 from:", ubergraph.get_from(u, "node1"))
    print("node1 to:", ubergraph.get_to(u, "node1"))
    print("node1 in edges:", ubergraph.get_in_edges(u, "node1"))
    print("node1 out edges:", ubergraph.get_out_edges(u, "node1"))
    
    print("node2 from:", ubergraph.get_from(u, "node2"))
    print("node2 to:", ubergraph.get_to(u, "node2"))
    print("node2 in edges:", ubergraph.get_in_edges(u, "node2"))
    print("node2 out edges:", ubergraph.get_out_edges(u, "node2"))
    
    print("node3 from:", ubergraph.get_from(u, "node3"))
    print("node3 to:", ubergraph.get_to(u, "node3"))
    print("node3 in edges:", ubergraph.get_in_edges(u, "node3"))
    print("node3 out edges:", ubergraph.get_out_edges(u, "node3"))

    print("edge1 from:", ubergraph.get_from(u, "edge1"))
    print("edge1 to:", ubergraph.get_to(u, "edge1"))
    print("edge1 in edges:", ubergraph.get_in_edges(u, "edge1"))
    print("edge1 out edges:", ubergraph.get_out_edges(u, "edge1"))
    
    print("edge2 from:", ubergraph.get_from(u, "edge2"))
    print("edge2 to:", ubergraph.get_to(u, "edge2"))
    print("edge2 in edges:", ubergraph.get_in_edges(u, "edge2"))
    print("edge2 out edges:", ubergraph.get_out_edges(u, "edge2"))
    

    u.layout()
    u.draw("file.png")