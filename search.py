import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation
from fontTools.unicodedata import block
import matplotlib; matplotlib.use("TkAgg")
from utils import *
from grid import *
from algorithms import *

def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons

if __name__ == "__main__":
    ascii_art = r"""

     _____                     _        ___  _                  _ _   _                   
    /  ___|                   | |      / _ \| |                (_) | | |                  
    \ `--.  ___  __ _ _ __ ___| |__   / /_\ \ | __ _  ___  _ __ _| |_| |__  _ __ ___  ___ 
     `--. \/ _ \/ _` | '__/ __| '_ \  |  _  | |/ _` |/ _ \| '__| | __| '_ \| '_ ` _ \/ __|
    /\__/ /  __/ (_| | | | (__| | | | | | | | | (_| | (_) | |  | | |_| | | | | | | | \__ \
    \____/ \___|\__,_|_|  \___|_| |_| \_| |_/_|\__, |\___/|_|  |_|\__|_| |_|_| |_| |_|___/
                                                __/ |                                     
                                               |___/                                      

        """
    print("WELCOME TO \n" + ascii_art)

    pathChoice = int(input("Choose the search grid Path first:\n 1. Default Path\n 2. Custom Path\n Enter Choice:"))
    if pathChoice == 1:
        epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
        tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')
        source = Point(8, 10)
        dest = Point(43, 45)
    elif pathChoice == 2:
        epolygons = gen_polygons('TestingGrid/enclosures.txt')
        tpolygons = gen_polygons('TestingGrid/turfs.txt')
        source = Point(15, 20)
        dest = Point(43, 45)
    else:
        print("Invalid choice")
        exit()


    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point
    
    # Draw enclosure polygons
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

    
    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

    obstacles = set()
    for polygon in epolygons:
        for point in polygon:
            obstacles.add(point.to_tuple())


    choiceNumber = input("Enter the search algorithm to use:\n 1. BFS\n 2. DFS\n 3. GBFS\n 4. A*\n Enter Choice:")
    choice = int(choiceNumber)
    if choice == 1:
        res_path = GridPathFinder(source, dest, epolygons, tpolygons).bfs()
    elif choice == 2:
        res_path = GridPathFinder(source, dest, epolygons, tpolygons).dfs()
    elif choice == 3:
        res_path = GridPathFinder(source, dest, epolygons, tpolygons).GBFS()
    elif choice == 4:
        res_path = GridPathFinder(source, dest, epolygons, tpolygons).aStar()
    else:
        print("Invalid choice")
        exit()

    for i in range(len(res_path)-1):
        draw_result_line(ax, [res_path[i].x, res_path[i+1].x], [res_path[i].y, res_path[i+1].y])
        plt.pause(0.1)

    plt.show()
