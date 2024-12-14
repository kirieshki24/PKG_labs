import customtkinter as ctk
import time
from math import cos, sin, pi
import tkinter as tk

class RasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Raster Algorithms")
        self.geometry("800x600")
        
        self.cell_size = 10 
        self.grid_size = 30  
        self.canvas_size = self.cell_size * (2 * self.grid_size + 1) 

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.canvas = tk.Canvas(self.canvas_frame, 
                              width=self.canvas_size, 
                              height=self.canvas_size, 
                              bg='white')
        self.canvas.pack(padx=10, pady=10)
        
        self.draw_grid()

        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.algorithm_var = ctk.StringVar(value="DDA")
        self.algorithm_label = ctk.CTkLabel(self.controls_frame, text="Algorithm:")
        self.algorithm_label.pack(pady=5)
        
        algorithms = ["DDA", "Bresenham Line", "Step by Step", "Bresenham Circle"]
        self.algorithm_menu = ctk.CTkOptionMenu(
            self.controls_frame,
            values=algorithms,
            variable=self.algorithm_var
        )
        self.algorithm_menu.pack(pady=5)

        self.coords_frame = ctk.CTkFrame(self.controls_frame)
        self.coords_frame.pack(pady=10)

        self.start_label = ctk.CTkLabel(self.coords_frame, text="Start point (x1, y1):")
        self.start_label.pack()
        
        self.x1_entry = ctk.CTkEntry(self.coords_frame, placeholder_text="x1")
        self.x1_entry.pack()
        
        self.y1_entry = ctk.CTkEntry(self.coords_frame, placeholder_text="y1")
        self.y1_entry.pack()

        self.end_label = ctk.CTkLabel(self.coords_frame, text="End point (x2, y2):")
        self.end_label.pack()
        
        self.x2_entry = ctk.CTkEntry(self.coords_frame, placeholder_text="x2")
        self.x2_entry.pack()
        
        self.y2_entry = ctk.CTkEntry(self.coords_frame, placeholder_text="y2")
        self.y2_entry.pack()

        range_text = f"Coordinate range: -{self.grid_size} to {self.grid_size}"
        self.range_label = ctk.CTkLabel(self.coords_frame, text=range_text)
        self.range_label.pack(pady=5)

        self.draw_button = ctk.CTkButton(
            self.controls_frame,
            text="Draw",
            command=self.draw
        )
        self.draw_button.pack(pady=10)

        self.clear_button = ctk.CTkButton(
            self.controls_frame,
            text="Clear",
            command=self.clear_canvas
        )
        self.clear_button.pack(pady=5)

        self.time_label = ctk.CTkLabel(self.controls_frame, text="Time: -")
        self.time_label.pack(pady=5)

    def draw_grid(self):
        for i in range(self.canvas_size + 1):
            if i % self.cell_size == 0:
                color = 'black' if i == self.canvas_size // 2 else 'lightgray'
                width = 2 if i == self.canvas_size // 2 else 1
                self.canvas.create_line(i, 0, i, self.canvas_size, fill=color, width=width)
                
                color = 'black' if i == self.canvas_size // 2 else 'lightgray'
                width = 2 if i == self.canvas_size // 2 else 1
                self.canvas.create_line(0, i, self.canvas_size, i, fill=color, width=width)

        for i in range(-self.grid_size, self.grid_size + 1, 5):
            x = self.canvas_size // 2 + i * self.cell_size
            self.canvas.create_text(x, self.canvas_size // 2 + 10, text=str(i), anchor="n")
            
            y = self.canvas_size // 2 - i * self.cell_size
            self.canvas.create_text(self.canvas_size // 2 + 10, y, text=str(i), anchor="w")
        
        self.canvas.create_line(
            0, self.canvas_size // 2, self.canvas_size, self.canvas_size // 2, fill="black", width=2
        )  
        self.canvas.create_line(
            self.canvas_size // 2, 0, self.canvas_size // 2, self.canvas_size, fill="black", width=2
        ) 


    def plot_pixel(self, x, y, color="black"):
        canvas_x = self.canvas_size // 2 + x * self.cell_size
        canvas_y = self.canvas_size // 2 - y * self.cell_size
        
        self.canvas.create_rectangle(
            canvas_x - self.cell_size//2,
            canvas_y - self.cell_size//2,
            canvas_x + self.cell_size//2,
            canvas_y + self.cell_size//2,
            fill=color,
            outline=color
        )

    def dda_line(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            self.plot_pixel(x1, y1)
            return
            
        x_increment = dx / steps
        y_increment = dy / steps
        
        x = x1
        y = y1
        
        for _ in range(int(steps) + 1):
            self.plot_pixel(int(x), int(y))  
            x += x_increment
            y += y_increment


    def bresenham_line(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx
            
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        y_step = 1 if y1 < y2 else -1
        error = dx // 2
        y = y1
        
        for x in range(x1, x2 + 1):
            if steep:
                self.plot_pixel(y, x)
            else:
                self.plot_pixel(x, y)
                
            error -= dy
            if error < 0:
                y += y_step
                error += dx

    def step_by_step(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            self.plot_pixel(x1, y1)
            return
            
        dx = x2 - x1
        dy = y2 - y1
        
        if abs(dx) >= abs(dy):
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            y = y1
            for x in range(x1, x2 + 1):
                self.plot_pixel(x, y)
                if dx != 0:
                    y = y1 + dy * (x - x1) // dx
        else:
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            x = x1
            for y in range(y1, y2 + 1):
                self.plot_pixel(x, y)
                if dy != 0:
                    x = x1 + dx * (y - y1) // dy

    def bresenham_circle(self, x_center, y_center, x2, y2):
        radius = int(((x2 - x_center) ** 2 + (y2 - y_center) ** 2) ** 0.5)
        x = 0
        y = radius
        d = 3 - 2 * radius
        
        def plot_circle_points(x, y):
            self.plot_pixel(x_center + x, y_center + y)
            self.plot_pixel(x_center - x, y_center + y)
            self.plot_pixel(x_center + x, y_center - y)
            self.plot_pixel(x_center - x, y_center - y)
            self.plot_pixel(x_center + y, y_center + x)
            self.plot_pixel(x_center - y, y_center + x)
            self.plot_pixel(x_center + y, y_center - x)
            self.plot_pixel(x_center - y, y_center - x)
        
        while y >= x:
            plot_circle_points(x, y)
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.time_label.configure(text="Time: -")

    def draw(self):
        try:
            x1 = int(self.x1_entry.get())
            y1 = int(self.y1_entry.get())
            x2 = int(self.x2_entry.get())
            y2 = int(self.y2_entry.get())
            
            # Check if coordinates are within range
            if max(abs(x1), abs(y1), abs(x2), abs(y2)) > self.grid_size:
                self.time_label.configure(text=f"Coordinates must be between -{self.grid_size} and {self.grid_size}")
                return
            
            start_time = time.time()
            
            algorithm = self.algorithm_var.get()
            if algorithm == "DDA":
                self.dda_line(x1, y1, x2, y2)
            elif algorithm == "Bresenham Line":
                self.bresenham_line(x1, y1, x2, y2)
            elif algorithm == "Step by Step":
                self.step_by_step(x1, y1, x2, y2)
            elif algorithm == "Bresenham Circle":
                self.bresenham_circle(x1, y1, x2, y2)
                
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            self.time_label.configure(text=f"Time: {execution_time:.2f} ms")
            
        except ValueError:
            self.time_label.configure(text="Invalid input!")

if __name__ == "__main__":
    app = RasterApp()
    app.mainloop()
