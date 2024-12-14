import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class Letter3DApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("3D Letter Visualization")
        self.geometry("1200x800")

        self.vertices = np.array([
            [0, 0, 0], [0, 5, 0], [1, 5, 0], [1, 0, 0],
            [0, 0, 1], [0, 5, 1], [1, 5, 1], [1, 0, 1],
            [1, 2.5, 0], [3, 5, 0], [4, 5, 0], [2, 2.5, 0],
            [1, 2.5, 1], [3, 5, 1], [4, 5, 1], [2, 2.5, 1],
            [1, 2.5, 0], [3, 0, 0], [4, 0, 0], [2, 2.5, 0],
            [1, 2.5, 1], [3, 0, 1], [4, 0, 1], [2, 2.5, 1]
        ])

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
            (8, 9), (9, 10), (10, 11), (11, 8),
            (12, 13), (13, 14), (14, 15), (15, 12),
            (8, 12), (9, 13), (10, 14), (11, 15),
            (16, 17), (17, 18), (18, 19), (19, 16),
            (20, 21), (21, 22), (22, 23), (23, 20),
            (16, 20), (17, 21), (18, 22), (19, 23)
        ]

        self.create_widgets()
        
        self.scale_factor = 1.0
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        
        self.transform_matrix = np.eye(4)
        
        self.update_visualization()
        
    #custom_font = ctk.CTkFont(family="Arial", size=20)

    def create_widgets(self):
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        scale_label = ctk.CTkLabel(control_frame, text="Масштаб:")
        scale_label.pack(pady=5)
        self.scale_slider = ctk.CTkSlider(control_frame, from_=0.1, to=2.0,number_of_steps=20, command=self.on_scale_change)
        self.scale_slider.set(1.0)
        self.scale_slider.pack(pady=5)

        translation_label = ctk.CTkLabel(control_frame, text="Перенос:")
        translation_label.pack(pady=5)
        for i, axis in enumerate(['X', 'Y', 'Z']):
            slider = ctk.CTkSlider(control_frame, from_=-5, to=5, number_of_steps=100, command=lambda val, axis=i: self.on_translation_change(val, axis))
            slider.set(0)
            slider.pack(pady=2)
            setattr(self, f'translation_slider_{axis}', slider)

        rotation_label = ctk.CTkLabel(control_frame, text="Вращение:")
        rotation_label.pack(pady=5)
        for i, axis in enumerate(['X', 'Y', 'Z']):
            slider = ctk.CTkSlider(control_frame, from_=0, to=360, number_of_steps=90, command=lambda val, axis=i: self.on_rotation_change(val, axis))
            slider.set(0)
            slider.pack(pady=2)
            setattr(self, f'rotation_slider_{axis}', slider)

        self.matrix_label = ctk.CTkLabel(control_frame, text="Матрица преобразования:", justify="left", font=('Arial', 20))
        self.matrix_label.pack(pady=10)

        self.fig = Figure(figsize=(12, 8))
        
        self.ax_3d = self.fig.add_subplot(221, projection='3d')
        
        self.ax_xy = self.fig.add_subplot(222)
        self.ax_xz = self.fig.add_subplot(223)
        self.ax_yz = self.fig.add_subplot(224)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def update_transform_matrix(self):
        scale_matrix = np.diag([self.scale_factor, self.scale_factor, self.scale_factor, 1])
        
        translation_matrix = np.eye(4)
        translation_matrix[:3, 3] = self.translation
        
        def rotation_matrix(axis, theta):
            theta = np.radians(theta)
            if axis == 0:  
                return np.array([
                    [1, 0, 0, 0],
                    [0, np.cos(theta), -np.sin(theta), 0],
                    [0, np.sin(theta), np.cos(theta), 0],
                    [0, 0, 0, 1]
                ])
            elif axis == 1:  
                return np.array([
                    [np.cos(theta), 0, np.sin(theta), 0],
                    [0, 1, 0, 0],
                    [-np.sin(theta), 0, np.cos(theta), 0],
                    [0, 0, 0, 1]
                ])
            else:  
                return np.array([
                    [np.cos(theta), -np.sin(theta), 0, 0],
                    [np.sin(theta), np.cos(theta), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ])

        rotation_x = rotation_matrix(0, self.rotation[0])
        rotation_y = rotation_matrix(1, self.rotation[1])
        rotation_z = rotation_matrix(2, self.rotation[2])
        
        self.transform_matrix = translation_matrix @ rotation_z @ rotation_y @ rotation_x @ scale_matrix
        
        matrix_text = "Матрица преобразования:\n"
        for row in self.transform_matrix:
            matrix_text += f"[{' '.join(f'{x:6.2f}' for x in row)}]\n"
        self.matrix_label.configure(text=matrix_text, )

    def transform_vertices(self):
        vertices_homogeneous = np.hstack((self.vertices, np.ones((len(self.vertices), 1))))
        
        transformed_vertices = vertices_homogeneous @ self.transform_matrix.T
        
        return transformed_vertices[:, :3]

    def update_visualization(self):
        transformed_vertices = self.transform_vertices()
        
        self.ax_3d.clear()
        self.ax_xy.clear()
        self.ax_xz.clear()
        self.ax_yz.clear()
        
        for edge in self.edges:
            self.ax_3d.plot3D(
                [transformed_vertices[edge[0]][0], transformed_vertices[edge[1]][0]],
                [transformed_vertices[edge[0]][1], transformed_vertices[edge[1]][1]],
                [transformed_vertices[edge[0]][2], transformed_vertices[edge[1]][2]],
                'blue'
            )
        
        for edge in self.edges:
            self.ax_xy.plot(
                [transformed_vertices[edge[0]][0], transformed_vertices[edge[1]][0]],
                [transformed_vertices[edge[0]][1], transformed_vertices[edge[1]][1]],
                'blue'
            )
            self.ax_xz.plot(
                [transformed_vertices[edge[0]][0], transformed_vertices[edge[1]][0]],
                [transformed_vertices[edge[0]][2], transformed_vertices[edge[1]][2]],
                'blue'
            )
            self.ax_yz.plot(
                [transformed_vertices[edge[0]][1], transformed_vertices[edge[1]][1]],
                [transformed_vertices[edge[0]][2], transformed_vertices[edge[1]][2]],
                'blue'
            )
        
        self.ax_3d.set_title('3D проекция')
        self.ax_xy.set_title('Проекция XY')
        self.ax_xz.set_title('Проекция XZ')
        self.ax_yz.set_title('Проекция YZ')
        
        limit = 6
        self.ax_3d.set_xlim([-limit, limit])
        self.ax_3d.set_ylim([-limit, limit])
        self.ax_3d.set_zlim([-limit, limit])
        self.ax_xy.set_xlim([-limit, limit])
        self.ax_xy.set_ylim([-limit, limit])
        self.ax_xz.set_xlim([-limit, limit])
        self.ax_xz.set_ylim([-limit, limit])
        self.ax_yz.set_xlim([-limit, limit])
        self.ax_yz.set_ylim([-limit, limit])
        
        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_xy.set_xlabel('X')
        self.ax_xy.set_ylabel('Y')
        self.ax_xz.set_xlabel('X')
        self.ax_xz.set_ylabel('Z')
        self.ax_yz.set_xlabel('Y')
        self.ax_yz.set_ylabel('Z')
        
        self.canvas.draw()

    def on_scale_change(self, value):
        self.scale_factor = float(value)
        self.update_transform_matrix()
        self.update_visualization()

    def on_translation_change(self, value, axis):
        self.translation[axis] = float(value)
        self.update_transform_matrix()
        self.update_visualization()

    def on_rotation_change(self, value, axis):
        self.rotation[axis] = float(value)
        self.update_transform_matrix()
        self.update_visualization()

if __name__ == "__main__":
    app = Letter3DApp()
    app.mainloop()
