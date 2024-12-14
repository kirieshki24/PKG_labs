import customtkinter as ctk
from tkinter import ttk, filedialog
from PIL import Image, TiffImagePlugin
import os
import threading

class ImageExtractor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Data Extractor")
        self.geometry("600x550")
        self.resizable(False, False)

        ctk.set_appearance_mode("green")
        ctk.set_default_color_theme("green")

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Size", "Resolution", "Color depth", "Compression"),
                                 show="headings", height=20)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")          
        self.tree.heading("Resolution", text="Resolution")
        self.tree.heading("Color depth", text="Color depth")
        self.tree.heading("Compression", text="Compression rate")

        self.tree.column("ID", width=60)
        self.tree.column("Name", width=150)
        self.tree.column("Size", width=100)
        self.tree.column("Resolution", width=100)
        self.tree.column("Color depth", width=100)
        self.tree.column("Compression", width=130)

        self.tree.pack(pady=20)

        self.directory_button = ctk.CTkButton(self, text="Выбрать директорию", command=self.start_directory_thread)
        self.directory_button.pack(pady=30)

        self.file_button = ctk.CTkButton(self, text="Выбрать файл", command=self.ask_file_button)
        self.file_button.pack(pady=10)

        self.counter = 1

    def calculate_compression_ratio(self, file_size, resolution):
        width, height = map(int, resolution.split('x'))
        uncompressed_size = width * height * 3  
        return max(round(((uncompressed_size - file_size) / uncompressed_size)*100), 0)
        
    def add_data(self, files):
        for file in files:
            name = os.path.basename(file)
            size = os.path.getsize(file)
            with Image.open(file) as img:
                width, height = img.size
                resolution = f"{width}x{height}"
                dpi = img.info.get('dpi')

                color_depth = {
                    '1': '1-bit',
                    'L': '8-bit',
                    'P': '8-bit',
                    'RGB': '3x8-bit',
                    'RGBA': '4x8-bit',
                    'CMYK': '4x8-bit',
                    'YCbCr': '3x8-bit',
                    'LAB': '3x8-bit',
                    'HSV': '3x8-bit',
                    'I': '32-bit',
                    'F': '32-bit'
                }.get(img.mode, f"Unknown ({img.mode})")
                compression = img.info.get('compression', 'No compression info')
                if name.lower().endswith((".jpeg", ".jpg")):
                    compression = self.calculate_compression_ratio(size, resolution)
                if isinstance(img, TiffImagePlugin.TiffImageFile):
                    compression = TiffImagePlugin.COMPRESSION_INFO.get(img.tag_v2.get(259), "No compression info")
            try:
                dpi = f'{int(dpi[0])} x {int(dpi[1])}'
            except:
                dpi = "N/A"
            self.tree.insert("", "end", values=(
                self.counter, name, resolution, 
                dpi, 
                color_depth, compression
            ))
            self.counter += 1

    def start_directory_thread(self):
        thread = threading.Thread(target=self.ask_directory_button)
        thread.start()

    def ask_directory_button(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        files = []
        for root, _, filenames in os.walk(directory):
            for file in filenames:
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".tif", ".bmp", ".pcx")):
                    files.append(os.path.join(root, file))

        self.add_data(files)

    def ask_file_button(self):
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.tif;*.bmp;*.pcx")])
        if file:
            self.add_data([file])

if __name__ == "__main__":
    app = ImageExtractor()
    app.mainloop()