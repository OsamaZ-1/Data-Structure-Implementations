import turtle
from random import randint

class maze:
    def __init__(self, d):
        self.t = turtle.Turtle()
        self.cells = []

        #d is the dimension of the maze, aka the number of cells in each row and col
        self.d = d
        #w is the width of each cell
        self.w = 10

        for i in range(d*d):
            self.cells.append(-1)

    def find(self, a):
        temp = a
        while self.cells[temp] > -1:
            temp = self.cells[temp]
        return temp

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return

        if self.cells[root_a] <= self.cells[root_b]:
            self.cells[root_a] += self.cells[root_b]
            self.cells[root_b] = root_a
        else:
            self.cells[root_b] += self.cells[root_a]
            self.cells[root_a] = root_b

    def draw_line(self, x1, y1, x2, y2):
        self.t.penup()
        self.t.goto(x1, y1)
        self.t.pendown()
        self.t.goto(x2, y2)

    def draw_parameter(self):
        self.draw_line(0, 0, self.d * self.w, 0)
        self.draw_line(self.d * self.w, self.w, self.d * self.w, self.d * self.w)
        self.draw_line(self.d * self.w, self.d * self.w, 0, self.d * self.w)
        self.draw_line(0, self.d * self.w - self.w, 0, 0)

    def draw_maze(self, walls):
        self.draw_parameter()
        for wall in walls:
            if wall[1] - wall[0] == 1:
                self.draw_line((wall[1] % self.d) * self.w, (self.d - (wall[1] // self.d)) * self.w, (wall[1] % self.d) * self.w, (self.d - (wall[1] // self.d) - 1) * self.w)
            else:
                self.draw_line((wall[0] % self.d) * self.w, (self.d - (wall[1] // self.d) - 1) * self.w, ((wall[0] % self.d) + 1) * self.w, (self.d - (wall[1] // self.d) - 1) * self.w)
        vs = self.t.getscreen()
        vs.mainloop()


def construct_relations(d):
    rel = []
    for i in range(d*d):
        if (i + 1) % d != 0:
            rel.append([i, i+1])
        if i not in range(d*d - d, d*d):
            rel.append([i, i+d])

    return rel

#main program:
d = 30
end = d * d - 1
m = maze(d)
relations = construct_relations(d)

while m.find(0) != m.find(end):
    randi = randint(0, len(relations) - 1)
    rel = relations.pop(randi)
    m.union(rel[0], rel[1])

m.draw_maze(relations)

