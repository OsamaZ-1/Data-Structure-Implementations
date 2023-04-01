from random import randint

class Node():
    def __init__(self, val, color = 1):
        self.val = val
        self.color = color          # 1 = red | 0 = black
        self.left = None
        self.right = None
        self.parent = None

    #display function is credited to J.V. from StackOverflow
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        if self.color == 0:
            c = "B"
        else:
            c = "R"
        
        # No child.
        if self.right is None and self.left is None:
            line = '%s:%s' % (self.val, c)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s:%s' % (self.val, c)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s:%s' % (self.val, c)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s:%s' % (self.val, c)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

class Red_Black_Tree():
    def __init__(self):
        self.nil = Node("N", 0)
        self.root = self.nil

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def fix_up_insert(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == 1:
                    uncle.color = 0
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 0
                    node.parent.parent.color = 1
                    self.left_rotate(node.parent.parent)
            if node == self.root:
                break
            self.root.color = 0


    def insert(self, val):
        node = Node(val)
        node.left = self.nil
        node.right = self.nil

        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if val > x.val:
                x = x.right
            else:
                x = x.left
        
        node.parent = y
        if y == self.nil:
            self.root = node
            node.color = 0
            return
        elif val < y.val:
            y.left = node
        else:
            y.right = node

        if node.parent == self.root:
            return
        self.fix_up_insert(node)

    def transplant(self, y, x):
        if y == self.root:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.parent = y.parent

    def fix_up_delete(self, x):
        while x != self.root and x.color == 0:
            if x.parent.left == x:
                w = x.parent.right
                #case 2
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    w = x.parent.right
                
                #case 3
                if w.right.color == 0 and w.left.color == 0:
                    w.color = 1
                    x = x.parent
                    if x.color == 1:
                        x.color = 0
                        return
                #case 4
                elif w.right.color == 0:
                    w.left.color = 0
                    w.color = 1
                    self.right_rotate(w)
                #case 5
                else:
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                #case 2
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    w = x.parent.left
                
                #case 3
                if w.right.color == 0 and w.left.color == 0:
                    w.color = 1
                    x = x.parent
                    if x.color == 1:
                        x.color = 0
                        return
                #case 4
                elif w.left.color == 0:
                    w.right.color = 0
                    w.color = 1
                    self.left_rotate(w)
                #case 5
                else:
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        #case 1
        x.color = 0

    def delete(self, val):
        node = self.root
        while node != self.nil and node.val != val:
            if val > node.val:
                node = node.right
            else:
                node = node.left
        if node == self.nil:
            return

        if node.left == self.nil:
            replace = node.right
            x = replace
            self.transplant(node, replace)
        elif node.right == self.nil:
            replace = node.left
            x = replace
            self.transplant(node, replace)
        else:
            replace = node.right
            while replace.left != self.nil:
                replace = replace.left
            x = replace.right
            self.transplant(replace, x)
            self.transplant(node, replace)
            if node.right != self.nil:
                node.right.parent = replace
            node.left.parent = replace
            replace.right = node.right
            replace.left = node.left

        if node.color == 1:
            if replace.color == 1 or replace == self.nil:
                return
            replace.color = 1
        else:
            if replace.color == 1:
                replace.color = 0
                return

        self.fix_up_delete(x)

    def print_tree(self):
        self.root.display()

#main
tree = Red_Black_Tree()
for i in range(20):
    tree.insert(randint(1, 50))

tree.print_tree()

