import tkinter as tk
import math

DEFAULT_POINTS = [(x*15, 200 * math.sin(x/10)) for x in range(1, 40)]
FPS = 30
FRAME_INTERVAL_MS = round(1000/FPS)


class TSPGADemo(tk.Frame):
    def __init__(self, cities_coords=DEFAULT_POINTS):
        self.master = tk.Tk()
        super().__init__(self.master)

        self.points = cities_coords
        self.canvas = tk.Canvas(self.master, width=500, height=500, bd=5, bg='white')
        self.canvas.pack()
        self.pack()
        self.time = 0
        self.master.after(FRAME_INTERVAL_MS, self.animate)

    def draw_points(self):
        [
            self.canvas.create_rectangle(x, y, x+1, y+1)
            for x, y in self.points[:self.time % len(self.points)]
        ]

    def draw(self):
        self.canvas.delete('all')
        self.draw_points()

    def update(self):
        self.time += 1

    def animate(self):
        self.draw()
        self.update()
        self.master.after(FRAME_INTERVAL_MS, self.animate)
