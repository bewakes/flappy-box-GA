import tkinter as tk
import math

DEFAULT_POINTS = [(x*15, 200 * math.sin(x/10)) for x in range(1, 40)]
FPS = 30
FRAME_INTERVAL_MS = round(1000/FPS)


class conf:
    top_margin = 10
    left_margin = 10
    canvas_height = 500
    canvas_width = 500
    title_height = 15
    title_frame_margin = 2
    widgets_offset_x = 15
    widgets_offset_y = 25

    def __init__(self):
        pass


class TSPGADemo(tk.Frame):
    def __init__(self, cities_coords=DEFAULT_POINTS):
        self.master = tk.Tk()
        super().__init__(self.master)
        self.points = cities_coords
        self.setup()
        self.time = 0
        self.master.after(FRAME_INTERVAL_MS, self.animate)

    def setup(self):
        # Setup population canvas
        x = conf.top_margin
        y = conf.left_margin

        title = tk.Label(self.master, text='Population')
        title.place(x=x, y=y)

        y += conf.title_frame_margin + conf.title_height

        self.population_canvas = tk.Canvas(self.master,
                                           width=conf.canvas_width,
                                           height=conf.canvas_height,
                                           bd=5, bg='white')
        self.population_canvas.place(x=x, y=y)
        y += conf.canvas_height + conf.widgets_offset_y

        # Setup control section
        control_title = tk.Label(self.master, text='Control')
        control_title.place(x=x, y=y)

        y += conf.title_height + conf.title_frame_margin

        # Setup within control frame
        self.control_frame = tk.Frame(self.master, highlightthickness=2,
                                      highlightbackground='#777')
        self.start_button = tk.Button(self.control_frame, text="Start")
        self.start_button.grid()
        # Setup control frame DONE

        # Place the control frame
        self.control_frame.place(x=x, y=y)

    def draw_points(self):
        [
            self.population_canvas.create_rectangle(x, y, x+1, y+1)
            for x, y in self.points[:self.time % len(self.points)]
        ]

    def draw(self):
        self.population_canvas.delete('all')
        self.draw_points()

    def update(self):
        self.time += 1

    def animate(self):
        self.draw()
        self.update()
        self.master.after(FRAME_INTERVAL_MS, self.animate)


if __name__ == '__main__':
    a = TSPGADemo()
    a.mainloop()
