import math
import random

import tkinter as tk

FPS = 80
FRAME_INTERVAL_MS = round(1000/FPS)

WIDTH = 900
HEIGHT = 450
OBSTACLES_H_SPACING = 350
OBSTACLES_V_SPACING = 175
OBSTACLES_WIDTH = 50
SPEED = 8
XSTEP = OBSTACLES_WIDTH + OBSTACLES_H_SPACING
FLAPPY_WIDTH = 28
FLAPPY_HEIGHT = 25
G = 0.6
OBSTACLES_START = 400

CHECK_STEP = 2

# For GA chromosomes

MIN_V = -40
MAX_V = 40

MIN_DX = -OBSTACLES_WIDTH  # Minimum distance that can be between bird and nearest obstacle
MAX_DX = OBSTACLES_H_SPACING  # Max distance that can be between bird and nearest obstacle

CHROMOSOME_STEP = 50  # This is for the array size

VSIZE = (MAX_V - MIN_V) // CHROMOSOME_STEP + 1
DYSIZE = 2*HEIGHT // CHROMOSOME_STEP + 1  # [-height, -height + 10, ... , 0, 10, 20, ... height]
DXSIZE = (MAX_DX - MIN_DX) // CHROMOSOME_STEP + 1


def random_color():
    color = ''.join([random.choice('0123456789abcdef') for _ in range(6)])
    return '#'+color


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


class Flappy():
    def __init__(self, x=20, y=HEIGHT/2, v=0, chromosome=[]):
        self.dead = False
        self.init_x, self.init_y, self.init_v = x, y, v
        self.y = y
        self.v = v
        self.chromosome = chromosome
        self.score = 0
        self.color = random_color()

    def reset(self):
        self.score = 0
        self.dead = 0
        self.x = self.init_x
        self.y = self.init_y
        self.v = self.init_v

    def should_jump(self, obstacles, curr_x):
        if not self.chromosome:
            return False

        # Get nearest obstacle
        nearest_obstacle = obstacles[0]
        for obstacle in obstacles:
            if self.x < curr_x(obstacle[0][0]):
                nearest_obstacle = obstacle
                break

        nearest_obstacle = obstacles[0]
        nearest_obstacle_upper_rect = nearest_obstacle[0]

        dx = self.x - nearest_obstacle_upper_rect[0]
        upper_dy = self.y - nearest_obstacle_upper_rect[3]

        i = math.ceil(dx - MIN_DX) // CHROMOSOME_STEP
        j = math.ceil(upper_dy + HEIGHT) // CHROMOSOME_STEP
        # k = math.ceil(self.v - MIN_V) // CHROMOSOME_STEP
        index = (j * DXSIZE + i)
        if index > len(self.chromosome):
            print('index greater')
            return False
        return self.chromosome[index] == 1

    def jump(self):
        self.v = -8

    def did_collide(self, obstacles, curr_x):
        return any([
            bounding_rect_collision(
                (self.x, self.y, self.x + FLAPPY_WIDTH, self.y + FLAPPY_HEIGHT),
                (curr_x(x1), y1, curr_x(x2), y2)
            )
            for obs in obstacles for (x1, y1, x2, y2) in obs
        ]) or self.y > HEIGHT or self.y < -FLAPPY_HEIGHT

    def update(self, time, obstacles, curr_x):
        if self.dead:
            return
        if self.did_collide(obstacles, curr_x):
            self.dead = True

        if time % CHECK_STEP == 0 and self.should_jump(obstacles, curr_x):
            self.jump()

        self.v += G
        self.y += self.v
        self.score += 1


class Game(tk.Frame):
    def __init__(self, play=True, genetic_algorithm=None):
        self.master = tk.Tk()
        super().__init__(self.master)
        self.generation = 0
        self.best_score_so_far = 0
        self.genetic_algorithm = genetic_algorithm

        self.play = play
        self.master.bind("<Key>", self.on_key)

        if not play and genetic_algorithm:
            self.birds = [Flappy(chromosome=p) for p in genetic_algorithm.population]
        else:
            self.birds = [Flappy()]

        self.setup()
        self.reset()
        self.animate()

    def reset(self):
        self._obstacles = [
            generate_obstacle(x)
            for x in range(OBSTACLES_START, 1200, OBSTACLES_WIDTH + OBSTACLES_H_SPACING)
        ]
        self.obstacles = read_obstacles()
        [bird.reset() for bird in self.birds]
        self.stop = False
        self.time = 0

    def setup(self):
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg='green')
        self.canvas.pack(pady=10)

        if self.play:
            self.button = tk.Button(self.master, text="Restart", command=self.restart)
            self.button.pack(pady=10)
        else:
            self.generation_counter = tk.StringVar()
            self.generation_container = tk.Label(self.master, textvariable=self.generation_counter, font='Helvetica 13 bold')
            self.generation_container.pack(pady=10)

            self.best_so_far = tk.StringVar()
            self.best_so_far_container = tk.Label(self.master, textvariable=self.best_so_far, font='Helvetica 14 bold')

            self.birds_scores = [tk.StringVar() for _ in self.birds]
            self.score_containers = [
                tk.Label(self.master, textvariable=self.birds_scores[x])
                for x in range(len(self.birds))
            ]
            for c in self.score_containers:
                c.pack()

            self.best_so_far_container.pack(pady=20)

    def restart(self):
        self.reset()
        self.animate()

    def next_run(self):
        # Move to next generation
        fitness = [bird.score for bird in self.birds]
        max_fitness = max(fitness)
        if max_fitness > self.best_score_so_far:
            self.best_score_so_far = max_fitness
        next_gen = self.genetic_algorithm.next_generation(fitness)
        self.birds = [Flappy(chromosome=x) for x in next_gen]
        self.reset()
        self.generation += 1
        self.animate()

    def on_key(self, event):
        if self.play and event.keysym == 'space':
            self.birds[0].jump()
        if self.genetic_algorithm and event.keysym == 'n':  # next gen
            self.next_run()

    def draw_flappy(self, bird):
        self.canvas.create_rectangle(
            bird.x, bird.y,
            bird.x + FLAPPY_WIDTH, bird.y + FLAPPY_HEIGHT,
            # fill=bird.color,
            fill='skyblue',
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

        if self.play:
            self.draw_flappy(self.birds[0])
        else:
            [self.draw_flappy(bird) for bird in self.birds if not bird.dead]

        self.generation_counter.set(f'Generation: {self.generation}')
        # Set scores
        for i, c in enumerate(self.birds_scores):
            c.set(f'Bird {i} Score:                      {self.birds[i].score}')

        self.best_so_far.set(f'Best Score so far: {self.best_score_so_far}')

    def curr_x(self, x):
        return x - self.time * SPEED

    def update(self):
        self.time += 1
        [bird.update(self.time, self.obstacles, self.curr_x) for bird in self.birds]

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
        self.stop = all([x.dead for x in self.birds])

    def animate(self):
        if (self.play and self.birds[0].dead):
            return
        if self.stop:
            self.next_run()
            return
        self.draw()
        self.update()
        self.master.after(FRAME_INTERVAL_MS, self.animate)


def generate_obstacles():
    with open('obstacles.data', 'w') as f:
        for i in range(5000):
            (a, b, c, d), (w, x, y, z) = generate_obstacle(OBSTACLES_START + i * (OBSTACLES_WIDTH + OBSTACLES_H_SPACING))
            f.write(f'{a} {b} {c} {d} {w} {x} {y} {z}\n')


def read_obstacles():
    obstacles = []
    with open('obstacles.data') as f:
        for line in f.readlines():
            a, b, c, d, e, ff, g, h = line.split()
            obstacles.append([
                (int(a), int(b), int(c), int(d)),
                (int(e), int(ff), int(g), int(h)),
            ])
    return obstacles[:100]


if __name__ == '__main__':
    from ga import GeneticAlgorithm

    genetic_alg = GeneticAlgorithm(
        population_size=24,
        crossover_rate=0.7,
        mutation_rate=0.09,
        chromosome_size=DYSIZE*DXSIZE,
    )

    game = Game(play=False, genetic_algorithm=genetic_alg)
    game.mainloop()
