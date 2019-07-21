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
    q_value_max = max([abs(world.agent.q[s.world_pos]
                           [world.agent.get_best_action(s).name] + s.reward)
                       for s in world.states])
    for s in world.states:
        # rendering state
        x = s.world_pos % world.width
        y = s.world_pos // world.width
        drawable = Rectangle(Point(grid['x1'] + x * grid['step_x'],
                                   grid['y1'] + y * grid['step_y']),
                             Point(grid['x1'] + (x + 1) * grid['step_x'],
                                   grid['y1'] + (y + 1) * grid['step_y']))
        q_s_value = abs(world.agent.q[s.world_pos]
                        [world.agent.get_best_action(s).name] + s.reward)
        drawable.setFill(color_rgb(63 - floor(63 * q_s_value / q_value_max),
                                   127 + floor(128 * q_s_value / q_value_max),
                                   63 - floor(63 * q_s_value / q_value_max)))
        drawable.draw(win)
        Text(Point(grid['x1'] + (x + 0.5) * grid['step_x'],
                   grid['y1'] + (y + 0.5) * grid['step_y']),
             str('%.3f' % s.value)).draw(win)
        Text(Point(grid['x1'] + (x + 0.5) * grid['step_x'],
                   grid['y1'] + (y + 0.7) * grid['step_y']),
             str('Reward = %.3f' % s.reward)).draw(win)


def main():
    w = World(4, 4)
    w.randomize_reward()
    win = GraphWin("My window", 500, 500, autoflush=False)
    win.setBackground('white')
    grid = grid_draw(10, 10, 490, 490, 4, 4, win)
    render(w, grid, win)
    while win.checkKey() != 'Escape':
        w.value_iteration()
        w.agent.step()
        render(w, grid, win)
        sleep(.033)
    win.close()


main()
