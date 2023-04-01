class disjoint_set:
    def __init__(self, n):
        self.set = []
        for _ in range(n):
            self.set.append(-1)

    def find_it(self, val):
        while self.set[val] > -1:
            val = self.set[val]
        return val

    def find_rec(self, val):
        if self.set[val] < 0:
            return val
        return self.find_rec(self.set[val])

    def path_comp_find(self, val):
        if self.set[val] < 0:
            return val
        root = self.path_comp_find(self.set[val])
        self.set[val] = root
        return root

    def union_basic(self, a, b):
        self.set[b] = a

    def union_by_size(self, a, b):
        root_a = self.find_it(a)
        root_b = self.find_it(b)
        if self.set[root_a] <= self.set[root_b]:
            self.set[root_a] += self.set[root_b]
            self.set[root_b] = root_a
        else:
            self.set[root_b] += self.set[root_a]
            self.set[root_a] = root_b

    def union_by_height(self, a, b):
        root_a = self.find_it(a)
        root_b = self.find_it(b)
        if self.set(root_a) == self.set(root_b):
            self.set[root_b] = root_a
            self.set[root_a] -= 1
        elif self.set[root_a] < self.set[root_b]:
            self.set[root_b] = root_a
        else:
            self.set[root_a] = root_b
            

ds = disjoint_set(8)
ds.union_basic(1, 2)
ds.union_basic(2, 3)
ds.union_basic(3, 7)
print(ds.set)
print(ds.path_comp_find(7))
print(ds.set)
print(ds.path_comp_find(4))
print(ds.set)

