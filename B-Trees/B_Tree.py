class Node:
    def __init__(self, leaf = False):
        self.keys = []
        self.c = []
        self.leaf = leaf

class B_Tree:
    def __init__(self, t):
        self.root = Node(True)
        self.t = t

    def search(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == k:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.search(node.c[i], k)

    def split(self, node, ch):
        child = node.c[ch]
        right = Node(child.leaf)

        node.keys = node.keys[: ch] + [child.keys[self.t - 1]] + node.keys[ch :]
        node.c = node.c[: ch + 1] + [right] + node.c[ch + 1 :]

        right.keys = child.keys[self.t :]
        child.keys = child.keys[: self.t - 1]
        if (not child.leaf):
            right.c = child.c[self.t :]
            child.c = child.c[: self.t]

    def insert(self, k):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            self.root = Node()
            self.root.c.append(r)
            self.split(self.root, 0)
        self.insert_no_full(self.root, k)

    def insert_no_full(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if (node.leaf):
            node.keys.insert(i, k)
        else:
            if len(node.c[i].keys) == 2 * self.t - 1:
                self.split(node, i)
                if node.keys[i] < k:
                    i += 1
            self.insert_no_full(node.c[i], k)

    def delete(self, node, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if (node.leaf):
            if i < len(node.keys) and k == node.keys[i]:
                node.keys.pop(i)
            return
        elif i < len(node.keys) and k == node.keys[i]:
            return self.delete_from_internal_node(node, i)
        elif len(node.c[i].keys) == t - 1:
            if i != 0 and i < len(node.keys):
                if len(node.c[i - 1].keys) > t - 1:
                    self.fix_by_sibling(node, i, i - 1)
                elif len(node.c[i + 1].keys) > t - 1:
                    self.fix_by_sibling(node, i, i + 1)
                else:
                    self.fix_by_merge(node, i, i + 1)
            elif i == 0:
                if len(node.c[i + 1].keys) > t - 1:
                    self.fix_by_sibling(node, i, i + 1)
                else:
                    self.fix_by_merge(node, i, i + 1)
            else:
                if len(node.c[i - 1].keys) > t - 1:
                    self.fix_by_sibling(node, i, i - 1)
                else:
                    self.fix_by_merge(node, i, i - 1)
            
        return self.delete(node.c[i], k)

    def fix_by_sibling(self, node, i, j):
        child = node.c[i]
        if i < j:
            right = node.c[j]
            child.keys.append(node.keys[i])
            node.keys[i] = right.keys.pop(0)
            if not right.leaf:
                child.c.append(right.c.pop(0))
        else:
            left = node.c[j]
            child.keys.insert(0, node.keys[i - 1])
            node.keys[i - 1] = left.keys.pop()
            if not left.leaf:
                child.c.insert(0, left.c.pop())

    def fix_by_merge(self, node, i, j):
        child = node.c[i]
        if i < j:
            right = node.c[j]
            child.keys.append(node.keys.pop(i))
            child.keys += right.keys                #Dr made a for loop and pop'd from the array while looping, does
            if not right.leaf:                      #that not cause any errors because of shifting the elements?
                child.c += right.c
            node.c.pop(j)
            newNode = child
        else:
            left = node.c[j]
            left.keys.append(node.keys.pop(j))
            left.keys += child.keys
            if not child.leaf:
                left.c += child.c
            node.c.pop(i)
            newNode = left
        
        if node == self.root and len(node.keys) == 0:
            self.root = newNode

    def delete_from_internal_node(self, node, i):
        t = self.t
        if len(node.c[i].keys) > t - 1:
            node.keys[i] = self.delete_predecessor(node.c[i])
        elif len(node.c[i + 1].keys) > t - 1:
            node.keys[i] = self.delete_successor(node.c[i + 1])
        else:
            self.fix_by_merge(node, i, i + 1)
            self.delete_from_internal_node(node.c[i], t - 1)

    def delete_predecessor(self, node):
        if node.leaf:
            return node.keys.pop()
        n = len(node.keys) - 1
        if len(node.c[n].keys) > self.t - 1:                #Why are we fixing the children even though their size is
            self.fix_by_sibling(node, n + 1, n)             #not < t-1 ?
        else:
            self.fix_by_merge(node, n, n + 1)
        return self.delete_predecessor(node.c[n])           #put recurssive call inside of if statement with n+1 (after fix_by_sibling)
                                                            #and with n in else (after merge)
    def delete_successor(self, node):
        if node.leaf:
            return node.keys.pop(0)
        if len(node.c[0].keys) > self.t - 1:
            self.fix_by_sibling(node, 0, 1)
        else:
            self.fix_by_merge(node, 0, 1)
        return self.delete_successor(node.c[0])


#main program:
b = B_Tree(2)
for i in range(1, 7):
    b.insert(i)
b.delete(b.root, 1)
print(b.root.keys)
print(b.root.c[0].keys)
print(b.root.c[1].keys)
print(b.root.c[2].keys)

