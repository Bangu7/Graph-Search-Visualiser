
def file_read(file):
    nodes = set()
    edges = []

    with open(file, "r") as f:
        for line in f.readlines():
            newline = line.strip().replace(" ", "").split(",")
            curNode = int(newline[0])
            nodes.add(curNode)
            for node in newline[1:]:
                node = int(node)
                edge = (curNode, node)
                if edge not in edges:
                    edges.append(edge)
                if node not in nodes:
                    nodes.add(node)
    
    return list(nodes), edges

# x, y = file_read("./ex1.txt")
# print(x)
# print(y)