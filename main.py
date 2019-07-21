from graphics.graphics import *
from rl.World import World
from time import sleep
from math import floor


def grid_draw(x1, y1, x2, y2, size_x, size_y, win):
    step_x = None
    step_y = None
    for i in range(0, size_y):
        step_y = (y2 - y1) / size_y
        for j in range(0, size_x):
            step_x = (x2 - x1) / size_x
            Rectangle(Point(x1 + step_x * j, y1 + step_y * i),
                      Point(x1 + step_x * (j + 1), y1 + step_y * (i + 1)))\
                .draw(win)
    return {
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'step_x': step_x,
        'step_y': step_y
    }


def render(world, grid, win):
    # rendering world states
    best_s_val = max([s.value for s in world.states])
    if best_s_val == 0: best_s_val = 1
    for s in world.states:
        # rendering state
        x = s.world_pos % world.width
        y = s.world_pos // world.width
        drawable = Rectangle(Point(grid['x1'] + x * grid['step_x'],
                                   grid['y1'] + y * grid['step_y']),
                             Point(grid['x1'] + (x + 1) * grid['step_x'],
                                   grid['y1'] + (y + 1) * grid['step_y']))
        drawable.setFill(color_rgb(63 - floor(63 * s.value / best_s_val),
                                   127 + floor(128 * s.value / best_s_val),
                                   63 - floor(63 * s.value / best_s_val)))
        drawable.draw(win)
        Text(Point(grid['x1'] + (x + 0.5) * grid['step_x'],
                   grid['y1'] + (y + 0.5) * grid['step_y']),
             '%.3f' % s.value).draw(win)
        Text(Point(grid['x1'] + (x + 0.5) * grid['step_x'],
                   grid['y1'] + (y + 0.7) * grid['step_y']),
             'Reward = %.3f' % s.reward).draw(win)
        # drawing a rectangular center over actions
        act_center = Rectangle(Point(grid['x1'] + (x + 0.475) * grid['step_x'],
                                     grid['y1'] + (y + 0.275) * grid['step_y']),
                               Point(grid['x1'] + (x + 0.525) * grid['step_x'],
                                     grid['y1'] + (y + 0.325) * grid['step_y']))
        act_center.setFill('red')
        # drawing action arrows
        arrows_length = 0.1
        arrows_points = lambda q_val: {
            'up': (Point(grid['x1'] + (x + 0.475) * grid['step_x'],
                         grid['y1'] + (y + 0.275) * grid['step_y']),
                   Point(grid['x1'] + (x + 0.525) * grid['step_x'],
                         grid['y1'] + (y + 0.275 - q_val / q_value_max * arrows_length)
                         * grid['step_y'])),
            'down': (Point(grid['x1'] + (x + 0.475) * grid['step_x'],
                           grid['y1'] + (y + 0.325) * grid['step_y']),
                     Point(grid['x1'] + (x + 0.525) * grid['step_x'],
                           grid['y1'] + (y + 0.325 + q_val / q_value_max * arrows_length)
                           * grid['step_y'])),
            'left': (Point(grid['x1'] + (x + 0.475 - q_val / q_value_max * arrows_length)
                           * grid['step_x'],
                           grid['y1'] + (y + 0.275) * grid['step_y']),
                     Point(grid['x1'] + (x + 0.475) * grid['step_x'],
                           grid['y1'] + (y + 0.325) * grid['step_y'])),
            'right': (Point(grid['x1'] + (x + 0.525) * grid['step_x'],
                            grid['y1'] + (y + 0.275) * grid['step_y']),
                      Point(grid['x1'] + (x + 0.525 + q_val / q_value_max * arrows_length)
                            * grid['step_x'],
                            grid['y1'] + (y + 0.325) * grid['step_y']))
        }

        q_value_max = max([abs(world.agent.q[s.world_pos][a.name]
                               + s.reward)
                           for a in s.actions.values()])
        for a in s.actions.values():
            q_value = abs(world.agent.q[s.world_pos][a.name] + s.reward)
            a_points = arrows_points(q_value)
            p1, p2 = a_points[a.name]
            arr = Rectangle(p1, p2)
            arr.setFill('black')
            arr.draw(win)
        act_center.draw(win)


def main():
    w = World(4, 4)
    w.randomize_reward()
    win = GraphWin("My window", 1000, 1000, autoflush=False)
    win.setBackground('white')
    grid = grid_draw(10, 10, 990, 990, 4, 4, win)
    render(w, grid, win)
    while win.checkKey() != 'Escape':
        w.value_iteration()
        w.agent.step()
        render(w, grid, win)
        sleep(.033)
    win.close()


main()
