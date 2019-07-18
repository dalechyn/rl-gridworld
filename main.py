from graphics.graphics import *
from rl import World

def grid_draw(x1, y1, x2, y2, size, win):
    for i in range(0, size):
        step_y = (y2 - y1) / size
        for j in range(0, size):
            step_x = (x2 - x1) / size
            Rectangle(Point(x1 + step_x * j, y1 + step_y * i),
                      Point(x1 + step_x * (j + 1), y1 + step_y * (i + 1))).draw(win)


def main():
    w = World.World(4, 4)
    w.build_gridworld()
    win = GraphWin("My window", 500, 500)
    print(win)
    win.setBackground('white')
    grid_draw(10, 10, 490, 490, 4, win)
    win.getMouse()
    win.close()


main()
