class Graph_Adjacency_Matrix:
    def __init__(self, num_v, undirected = False):
        self.undirected = undirected
        self.num_v = num_v
        self.matrix = []
        for _ in range(num_v):
            self.matrix.append([0] * num_v)

    def add_edge(self, v1, v2):
        if v1 < 0 or v1 > self.num_v - 1 or v2 < 0 or v2 > self.num_v - 1:
            print("Vertex not found.")
            return
        self.matrix[v1][v2] = 1
        if self.undirected:
            self.matrix[v2][v1] = 1

    def get_adjacent_verticies(self, v):
        if v < 0 or v > self.num_v - 1:
            print("Vertex not found.")
            return
        a = []
        for j in range(self.num_v):
            if self.matrix[v][j] == 1:
                a.append(j)
        return a

    def dfs_func(self, v, visited):
        print(v)
        visited[v] = True
        adj = self.get_adjacent_verticies(v)
        for n in adj:
            if not visited[n]:
                self.dfs_func(n, visited)

    def dfs(self):
        visited = [False] * self.num_v
        for i in range(self.num_v):
            if not visited[i]:
                self.dfs_func(i, visited)
                print("\n")

    def bfs(self):
        visited = [False] * self.num_v
        queue = []
        for i in range(self.num_v):
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                print("\n")
            while len(queue) > 0:
                v = queue.pop(0)
                print(v)
                adj = self.get_adjacent_verticies(v)
                for n in adj:
                    if not visited[n]:
                        queue.append(n)
                        visited[n] = True

#main
g = Graph_Adjacency_Matrix(7, True)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(4, 3)
g.add_edge(4, 2)
g.add_edge(5, 6)
g.bfs()

