import pandas as pd

def insert(canvas, pos, string, scale=2):
    x = pos[0]
    y = pos[1]
    canvas[y] = canvas[y][:x] + string + canvas[y][x+len(string):]
    return canvas

def insert_end(canvas, row_idx, string):
    canvas[row_idx] += string
    return canvas

class Graph:

    def __init__(self, connections, vertices):
        self.canvas = None
        self.gen_graf(connections, vertices)

    def gen_graf(self, connections, vertices):
        xoffset = 6
        spacing = 1
        scale = spacing + 1
        raw_size = vertices['ver'].max()[0]
        size = raw_size * scale + 1 
        #Generate self.canvas
        self.canvas = [' ' * (size + xoffset)] * size

        # end setup

        for i in range(len(vertices)):
            ver = vertices.iloc[i]['ver']
            ver_type = '@' if vertices.iloc[i]['type'] == 0 else 'O'
            x = ver[1]*scale + xoffset 
            y = ver[0]*scale
            self.canvas = insert(self.canvas, [x,y], ver_type, scale) 
            if ver[1] == ver[0]:
                self.canvas = insert(self.canvas, [x-1,y], '←', scale)
                xn = "x" + str(ver[0])
                self.canvas = insert(self.canvas, [x-2 - len(xn),y], xn, scale)
            
            if ver[1] == raw_size:
                self.canvas = insert_end(self.canvas, y, "← b" + str(ver[0]))


        for idx, con in connections.iterrows():
            fr = con['from']
            to = con['to']

            diff = [
                fr[1] - to[1], # 1 -> x ponieważ j jest na osi x
                fr[0] - to[0], # 0 -> y
            ]

            if diff[0] > 0:
                x = to[1] * scale + 1 + xoffset
                y = to[0] * scale
                self.canvas = insert(self.canvas, [x,y], '←', scale)
            if diff[1] > 0:
                x = to[1] * scale + xoffset
                y = to[0] * scale + 1
                self.canvas = insert(self.canvas, [x,y], '↑', scale)
                
    def print(self):
        for row in self.canvas:
            print(row)
