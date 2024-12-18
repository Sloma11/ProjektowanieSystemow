import sys
import sdl2.ext
import pandas as pd

def draw_ver(surface, pos, color):
    size = 20
    w, h = size,size
    half = size // 2
    sdl2.ext.fill(surface, color, (pos[0]-half, pos[1]-half, w, h))

def real_pos(pos):
    spacing = 50
    x = pos[0] * spacing + 10
    y = pos[1] * spacing + 10
    return [x, y]

def draw_conn(surface, pos1, pos2):
    sdl2.ext.line(surface, 0, (pos1[0], pos1[1], pos2[0], pos2[1]), 1)
    triangle_size = 8

    sdl2.ext.line(surface, 0, (pos1[0]+triangle_size, pos1[1], pos2[0], pos2[1]), 1)
    sdl2.ext.line(surface, 0, (pos1[0]-triangle_size, pos1[1], pos2[0], pos2[1]), 1)
    sdl2.ext.line(surface, 0, (pos1[0], pos1[1]+triangle_size, pos2[0], pos2[1]), 1)
    sdl2.ext.line(surface, 0, (pos1[0], pos1[1]-triangle_size, pos2[0], pos2[1]), 1)

    # sdl2.ext.line(surface, 0, (pos1[0]+1, pos1[1], pos2[0]+1, pos2[1]), 1)
    # sdl2.ext.line(surface, 0, (pos1[0]-1, pos1[1], pos2[0]-1, pos2[1]), 1)
    # sdl2.ext.line(surface, 0, (pos1[0], pos1[1]+1, pos2[0], pos2[1]+1), 1)
    # sdl2.ext.line(surface, 0, (pos1[0], pos1[1]-1, pos2[0], pos2[1]-1), 1)
    
def draw_graph(verts, connections):
    RESOURCES = sdl2.ext.Resources(__file__, "resources")

    sdl2.ext.init()

    window = sdl2.ext.Window("Hello World!", size=(1280, 720))
    window.show()
    win_surface = window.get_surface()
    sdl2.ext.fill(win_surface, sdl2.ext.Color(255,255,255))

    red = sdl2.ext.Color(255,0,0)
    gray = sdl2.ext.Color(128,128,128)

    vert_list = {'pos': [], 'type': []}
    connection_list = {'pos1': [], 'pos2': []}
    # world_offset = [0,0]
    # exit_event = False

    for idx in range(verts.shape[0]):
        ver = verts.iloc[idx]
        vert_list['pos'].append(real_pos([ver['i'], ver['j']]))
        vert_list['type'].append(verts.iloc[idx].loc['type'])
    verts = pd.DataFrame(data=vert_list)

    for idx in range(connections.shape[0]):
        row = connections.iloc[idx]
        connection_list['pos1'].append(real_pos(row.loc['from']))
        connection_list['pos2'].append(real_pos(row.loc['to']))
    connections = pd.DataFrame(data=connection_list)
    
    for i in range(connections.shape[0]):
        row = connections.iloc[i]
        draw_conn(win_surface, row.loc['pos1'], row.loc['pos2'])

    for i in range(verts.shape[0]):
        row = verts.iloc[i]
        color = gray if row.loc['type'] == 1 else red
        draw_ver(win_surface, row.loc['pos'], color)

        
    window.refresh()
    processor = sdl2.ext.TestEventProcessor()
    processor.run(window)




