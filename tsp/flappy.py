import tkinter as tk

import random

FPS = 30
FRAME_INTERVAL_MS = round(1000/FPS)

WIDTH = 900
HEIGHT = 450
OBSTACLES_H_SPACING = 220
OBSTACLES_V_SPACING = 175
OBSTACLES_WIDTH = 50
SPEED = 8
XSTEP = OBSTACLES_WIDTH + OBSTACLES_H_SPACING
FLAPPY_WIDTH = 28
FLAPPY_HEIGHT = 25


def generate_obstacle(x: int):
    """Returns obstacle bounds for obstacle """
    upper_y = random.randrange(10, HEIGHT - OBSTACLES_V_SPACING - 10)
    return [
        (x, 0, x+OBSTACLES_WIDTH, upper_y),
        (x, upper_y + OBSTACLES_V_SPACING, x+OBSTACLES_WIDTH, HEIGHT)
    ]


def bounding_rect_collision(rect_a, rect_b):
    ax1, ay1, ax2, ay2 = rect_a
    bx1, by1, bx2, by2 = rect_b
    return (ax1 <= bx2 and ax1 >= bx1 and ay1 <= by2 and ay1 >= by1) or\
           (ax2 <= bx2 and ax2 >= bx1 and ay2 <= by2 and ay2 >= by1)


class Flappy(tk.Frame):
    def __init__(self):
        self.master = tk.Tk()
        super().__init__(self.master)
        self.master.bind("<Key>", self.on_key)
        self.reset()
        self.setup()
        self.animate()

    def setup(self):
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg='white')
        self.canvas.pack(pady=10)
        self.button = tk.Button(self.master, text="Restart", command=self.reset)
        self.button.pack(pady=10)
        self.score_label = tk.Label(self.master, text="Score")
        self.score_label.pack(pady=10)
        self.score = tk.StringVar()
        self.score_container = tk.Label(self.master, textvariable=self.score)
        self.score_container.pack()

    def did_collide(self):
        return any([
            bounding_rect_collision(
                (self.x, self.y, self.x + FLAPPY_WIDTH, self.y + FLAPPY_HEIGHT),
                (self.curr_x(x1), y1, self.curr_x(x2), y2)
            )
            for obs in self.obstacles for (x1, y1, x2, y2) in obs
        ]) or self.y > HEIGHT or self.y < -FLAPPY_HEIGHT

    def on_key(self, event):
        if event.keysym == 'space':
            self.v = -8

    def reset(self):
        self.time = 0

        self.obstacles = [
            generate_obstacle(x)
            for x in range(300, 1000, OBSTACLES_WIDTH + OBSTACLES_H_SPACING)
        ]
        self.a = 0.6
        self.v = 0
        self.x = 20
        self.y = HEIGHT / 2

    def draw_flappy(self):
        self.canvas.create_rectangle(
            self.x, self.y,
            self.x + FLAPPY_WIDTH, self.y + FLAPPY_HEIGHT,
            fill='green'
        )

    def draw_obstacles(self):
        for upper, lower in self.obstacles:
            x1, y1, x2, y2 = upper
            self.canvas.create_rectangle(
                x1-self.time*SPEED, y1, x2-self.time*SPEED, y2, fill='brown'
            )
            lx1, ly1, lx2, ly2 = lower
            self.canvas.create_rectangle(
                lx1-self.time*SPEED, ly1, lx2-self.time*SPEED, ly2, fill='brown'
            )

    def draw(self):
        self.canvas.delete('all')
        self.draw_obstacles()
        self.draw_flappy()
        # Set score
        self.score.set(str(self.time))

    def curr_x(self, x):
        return x - self.time * SPEED

    def update(self):
        if self.did_collide():
            return

        self.v += self.a
        self.y += self.v
        self.time += 1

        # Filter obstacles and create new if necessary
        self.obstacles = [
            x for x in self.obstacles
            if self.curr_x(x[0][0]) + OBSTACLES_WIDTH >= 0
        ]
        obstacles_count = len(self.obstacles)
        obstacles_buffer_size = 10  # TODO: this is configurable/global

        if obstacles_count < obstacles_buffer_size:
            # add new obstacles, Assumes, there is at least 1 obstacle
            last_obs_x = self.obstacles[-1][0][0]
            diff = obstacles_buffer_size - obstacles_count
            x_range = (last_obs_x+XSTEP, last_obs_x + diff * XSTEP)
            self.obstacles = [
                *self.obstacles,
                *[
                    generate_obstacle(x)
                    for x in range(*x_range, XSTEP)
                ]
            ]

    def animate(self):
        self.draw()
        self.update()
        self.master.after(FRAME_INTERVAL_MS, self.animate)


if __name__ == '__main__':
    flappy = Flappy()
    flappy.mainloop()
