import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    algorithm_type = int(lines[0].strip())  # 1 for Cohen-Sutherland, 2 for Cyrus-Beck
    n = int(lines[1].strip())
    
    if algorithm_type == 1:  # Cohen-Sutherland
        segments = [list(map(float, line.strip().split())) for line in lines[2:n + 2]]
        clipping_window = list(map(float, lines[n + 2].strip().split()))
        return algorithm_type, segments, clipping_window, None
    else:  # Cyrus-Beck
        line = list(map(float, lines[2].strip().split()))  # Single line to clip
        m = int(lines[3].strip())  # Number of vertices in clipping polygon
        clipping_polygon = [list(map(float, line.strip().split())) for line in lines[4:m + 4]]
        return algorithm_type, [line], None, clipping_polygon

def cyrus_beck_clip(line, clip_polygon):
    def dot_product(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    x1, y1, x2, y2 = line
    P1 = np.array([x1, y1])
    P2 = np.array([x2, y2])
    D = P2 - P1  # Direction vector

    n = len(clip_polygon)
    normals = []
    
    # Calculate normal vectors for each edge
    for i in range(n):
        edge_start = np.array(clip_polygon[i])
        edge_end = np.array(clip_polygon[(i + 1) % n])
        edge = edge_end - edge_start
        normal = np.array([-edge[1], edge[0]])  # Perpendicular vector
        normal = normal / np.linalg.norm(normal)  # Normalize
        normals.append(normal)

    t_enter = 0.0
    t_exit = 1.0

    for i in range(n):
        edge_start = np.array(clip_polygon[i])
        normal = normals[i]
        
        numerator = dot_product(normal, (edge_start - P1))
        denominator = dot_product(normal, D)

        if denominator == 0:  # Line is parallel to this edge
            if numerator < 0:  # Line is outside
                return None
            continue

        t = numerator / denominator

        if denominator > 0:  # Entering
            t_enter = max(t_enter, t)
        else:  # Exiting
            t_exit = min(t_exit, t)

        if t_enter > t_exit:
            return None

    if t_enter > t_exit:
        return None

    # Calculate clipped points
    clipped_start = P1 + t_enter * D
    clipped_end = P1 + t_exit * D

    return [clipped_start[0], clipped_start[1], clipped_end[0], clipped_end[1]]

def cohen_sutherland_clip(line, window):
    # ... (keep existing Cohen-Sutherland implementation)
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    xmin, ymin, xmax, ymax = window

    def compute_code(x, y):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code

    x1, y1, x2, y2 = line
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            if code1 != 0:
                out_code = code1
            else:
                out_code = code2

            if out_code & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif out_code & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif out_code & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif out_code & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if out_code == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)

    if accept:
        return [x1, y1, x2, y2]
    else:
        return None

def visualize(algorithm_type, segments, clipping_window, clipping_polygon, clipped_segments, canvas_frame):
    fig, ax = plt.subplots(figsize=(6, 6))

    if algorithm_type == 1:  # Cohen-Sutherland
        xmin, ymin, xmax, ymax = clipping_window
        rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                           edgecolor='red', facecolor='none', linewidth=2, label='Отсекающее окно')
        ax.add_patch(rect)
    else:  # Cyrus-Beck
        polygon_np = np.array(clipping_polygon)
        polygon_patch = Polygon(polygon_np, closed=True, edgecolor='red',
                              facecolor='none', linewidth=2, label='Отсекающий многоугольник')
        ax.add_patch(polygon_patch)

    for i, segment in enumerate(segments):
        x1, y1, x2, y2 = segment
        if i == 0:
            ax.plot([x1, x2], [y1, y2], 'b--', label='Исходные отрезки')
        else:
            ax.plot([x1, x2], [y1, y2], 'b--')

    for i, segment in enumerate(clipped_segments):
        if segment:
            x1, y1, x2, y2 = segment
            if i == 0:
                ax.plot([x1, x2], [y1, y2], 'g-', label='Отсечённые отрезки')
            else:
                ax.plot([x1, x2], [y1, y2], 'g-')

    ax.set_aspect('equal')
    ax.legend(loc='upper right')

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def main_application():
    def select_file():
        file_path = filedialog.askopenfilename(title="Выберите входной файл",
                                             filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
        if file_path:
            file_label.configure(text=file_path)
            process_file(file_path)

    def process_file(file_path):
        try:
            algorithm_type, segments, clipping_window, clipping_polygon = read_file(file_path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")
            return

        if algorithm_type == 1:  # Cohen-Sutherland
            clipped_segments = [cohen_sutherland_clip(segment, clipping_window) for segment in segments]
            visualize(algorithm_type, segments, clipping_window, None, clipped_segments, canvas_frame)
        else:  # Cyrus-Beck
            clipped_segments = [cyrus_beck_clip(segment, clipping_polygon) for segment in segments]
            visualize(algorithm_type, segments, None, clipping_polygon, clipped_segments, canvas_frame)

    app = ctk.CTk()
    app.title("Визуализация Алгоритмов Отсечения")
    app.geometry("800x600")

    control_frame = ctk.CTkFrame(app)
    control_frame.pack(side='top', fill='x', padx=10, pady=10)

    select_button = ctk.CTkButton(control_frame, text="Выбрать Входной Файл", command=select_file)
    select_button.pack(side='left', padx=5)

    file_label = ctk.CTkLabel(control_frame, text="Файл не выбран")
    file_label.pack(side='left', padx=5)

    canvas_frame = ctk.CTkFrame(app)
    canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main_application()
