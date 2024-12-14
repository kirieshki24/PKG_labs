import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ImageProcessingApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Image Processing")
        self.app.geometry("1200x800")
        
        self.original_image = None
        self.processed_image = None
        self.current_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self.app)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.left_panel = ctk.CTkFrame(self.main_container, width=300)
        self.left_panel.pack(side="left", fill="y", padx=5, pady=5)
        
        self.load_btn = ctk.CTkButton(
            self.left_panel, 
            text="Load Image", 
            command=self.load_image
        )
        self.load_btn.pack(pady=10, padx=10)
        
        self.smoothing_frame = ctk.CTkFrame(self.left_panel)
        self.smoothing_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.smoothing_frame, text="Smoothing Filters").pack()
        
        self.kernel_size_var = ctk.IntVar(value=3)
        ctk.CTkLabel(self.smoothing_frame, text="Kernel Size:").pack()
        self.kernel_slider = ctk.CTkSlider(
            self.smoothing_frame,
            from_=3,
            to=100,
            number_of_steps=98,
            variable=self.kernel_size_var,
            command=self.update_kernel_size
        )
        self.kernel_slider.pack(pady=5)
        self.kernel_size_label = ctk.CTkLabel(self.smoothing_frame, text="3x3")
        self.kernel_size_label.pack()
        
        self.average_btn = ctk.CTkButton(
            self.smoothing_frame,
            text="Average Filter",
            command=self.apply_average_filter
        )
        self.average_btn.pack(pady=5)
        
        self.gaussian_btn = ctk.CTkButton(
            self.smoothing_frame,
            text="Gaussian Filter",
            command=self.apply_gaussian_filter
        )
        self.gaussian_btn.pack(pady=5)
        
        self.histogram_frame = ctk.CTkFrame(self.left_panel)
        self.histogram_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.histogram_frame, text="Histogram Processing").pack()
        
        self.min_intensity = ctk.IntVar(value=0)
        self.max_intensity = ctk.IntVar(value=255)
        
        ctk.CTkLabel(self.histogram_frame, text="Min Intensity:").pack()
        self.min_slider = ctk.CTkSlider(
            self.histogram_frame,
            from_=0,
            to=255,
            variable=self.min_intensity,
        )
        self.min_slider.pack(pady=5)
        
        ctk.CTkLabel(self.histogram_frame, text="Max Intensity:").pack()
        self.max_slider = ctk.CTkSlider(
            self.histogram_frame,
            from_=0,
            to=255,
            variable=self.max_intensity,
        )
        self.max_slider.pack(pady=5)
        
        self.contrast_btn = ctk.CTkButton(
            self.histogram_frame,
            text="Apply Linear Contrast",
            command=self.apply_linear_contrast
        )
        self.contrast_btn.pack(pady=5)
        
        self.equalize_btn = ctk.CTkButton(
            self.histogram_frame,
            text="Equalize Histogram",
            command=self.apply_histogram_equalization
        )
        self.equalize_btn.pack(pady=5)
        
        self.reset_btn = ctk.CTkButton(
            self.left_panel,
            text="Reset Image",
            command=self.reset_image
        )
        self.reset_btn.pack(pady=10)
        
        self.save_btn = ctk.CTkButton(
            self.left_panel,
            text="Save Image",
            command=self.save_image
        )
        self.save_btn.pack(pady=10)
        
        self.right_panel = ctk.CTkFrame(self.main_container)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.image_label = ctk.CTkLabel(self.right_panel, text="Load an image to begin")
        self.image_label.pack(expand=True)
        
        self.hist_canvas = None

    def update_kernel_size(self, value):
        size = int(value)
        if size % 2 == 0:
            size += 1
        self.kernel_size_var.set(size)
        self.kernel_size_label.configure(text=f"{size}x{size}")
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        try:
            if file_path:
                self.original_image = cv2.imread(file_path)
                self.current_image = self.original_image.copy()
                self.image_label.configure(text="")
                self.update_image_display()
        except:
            self.image_label.configure(text="Invalid path to image")
            
    def update_image_display(self):
        if self.current_image is not None:
            image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            
            display_size = (800, 600)
            h, w = image_rgb.shape[:2]
            aspect = w/h
            
            if aspect > display_size[0]/display_size[1]:
                new_w = display_size[0]
                new_h = int(new_w/aspect)
            else:
                new_h = display_size[1]
                new_w = int(new_h*aspect)
                
            image_resized = cv2.resize(image_rgb, (new_w, new_h))
            
            image_pil = Image.fromarray(image_resized)
            image_tk = ImageTk.PhotoImage(image_pil)
            
            self.image_label.configure(image=image_tk)
            self.image_label.image = image_tk
            
            self.update_histogram()

    def update_histogram(self):
        if self.current_image is not None:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

            fig, ax = plt.subplots(figsize=(6, 2))
            ax.plot(histogram, color='black')
            ax.set_xlim([0, 256])
            ax.set_title('Histogram')
            ax.set_xlabel('Pixel Intensity')
            ax.set_ylabel('Frequency')

            if self.hist_canvas:
                self.hist_canvas.get_tk_widget().destroy()

            self.hist_canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
            self.hist_canvas.get_tk_widget().pack(fill="x", padx=5, pady=5)
            self.hist_canvas.draw()
            plt.close(fig)
            
    def apply_average_filter(self):
        if self.current_image is not None:
            kernel_size = self.kernel_size_var.get()
            kernel = np.ones((kernel_size, kernel_size), np.float32)/(kernel_size**2)
            self.current_image = cv2.filter2D(self.current_image, -1, kernel)
            self.update_image_display()
            
    def apply_gaussian_filter(self):
        if self.current_image is not None:
            kernel_size = self.kernel_size_var.get()
            self.current_image = cv2.GaussianBlur(
                self.current_image, 
                (kernel_size, kernel_size),
                0
            )
            self.update_image_display()
            
            
    def apply_linear_contrast(self):
        if self.current_image is not None:
            min_val = self.min_intensity.get()
            max_val = self.max_intensity.get()
            
            if min_val >= max_val:
                min_val = max_val - 1
                self.min_intensity.set(min_val)
            
            img_float = self.current_image.astype(float)
            img_stretched = (img_float - min_val) * (255.0/(max_val - min_val))
            img_stretched = np.clip(img_stretched, 0, 255)
            self.current_image = img_stretched.astype(np.uint8)
            self.update_image_display()
            
    def apply_histogram_equalization(self):
        if self.current_image is not None:
            img_yuv = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2YUV)
            
            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
            
            self.current_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            self.update_image_display()
            
    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.update_image_display()
            
    def save_image(self):
        if self.current_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
            )
            if file_path:
                cv2.imwrite(file_path, self.current_image)
                
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.run()
