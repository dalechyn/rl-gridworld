from graphics.graphics import *
from rl import World


def grid_draw(x1, y1, x2, y2, size_x, size_y, win):
    for i in range(0, size_y):
        step_y = (y2 - y1) / size_y
        for j in range(0, size_x):
            step_x = (x2 - x1) / size_x
            Rectangle(Point(x1 + step_x * j, y1 + step_y * i),
                      Point(x1 + step_x * (j + 1), y1 + step_y * (i + 1))).draw(win)
    return {
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'size_x': size_x,
        'size_y': size_y
    }

def render(world, grid, win):
    # rendering world states
    for s in world.states:
        # rendering state
        x = s.world_pos % world.width
        y = s.world_pos / world.width
        drawable = Rectangle(Point(grid['x1'] + x * grid['size_x'], grid['y1'] + y * grid['size_y']),
                  Point(grid['x1'] + (x + 1) * grid['size_x'], grid['y1'] + (y + 1) * grid['size_y']))
        #drawable.setFill(color_rgb())


def main():
    w = World.World(4, 4)
    w.build_gridworld()
    win = GraphWin("My window", 500, 500)
    win.setBackground('white')
    grid = grid_draw(10, 10, 490, 490, 4, 4, win)
    render(w, grid, win)
    win.getMouse()
    win.close()


main()
