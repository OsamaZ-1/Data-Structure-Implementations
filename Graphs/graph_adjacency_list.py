class Vertex:
    def __init__(self, val):
        self.val = val
        self.next = None

class Adjacency_List:
    def __init__(self, root_val):
        self.root = Vertex(root_val)
        self.tail = self.root

    def add_edge(self, v):
        nv = Vertex(v)
        self.tail.next = nv
        self.tail = nv

    def get_adjacent_vertecies(self):
        a = []
        temp = self.root.next
        while temp != None:
            a.append(temp.val)
            temp = temp.next
        return a

class Graph_Adjacency_List:
    def __init__(self, num_v, undirected = False):
        self.num_v = num_v
        self.undirected = undirected
        self.lists = []
        for i in range(num_v):
            self.lists.append(Adjacency_List(i))

    def add_edge(self, v1, v2):
        if v1 < 0 or v1 > self.num_v - 1 or v2 < 0 or v2 > self.num_v - 1:
            print("Vertex not found.")
            return
        self.lists[v1].add_edge(v2)
        if self.undirected:
            self.lists[v2].add_edge(v1)

    def get_adjacent_vertecies(self, v):
        if v < 0 or v > self.num_v - 1:
            print("Vertex not found.")
            return
        return self.lists[v].get_adjacent_vertecies()

#main
g = Graph_Adjacency_List(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 2)
g.add_edge(2, 3)

for i in range (4):
    print(g.get_adjacent_vertecies(i))

