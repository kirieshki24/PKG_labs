import customtkinter as ctk
from tkinter import Canvas
from CTkColorPicker import *

def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (1, 3, 5))
def rgb_to_hex(r, g, b):  
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def entry_validator(a, b, entry):
    x = entry.get()
    if '.' in x:
        if float(x) < a:
            return a
        if float(x) > b:
            return b
        return float(x)
    else:
        if int(x) < a:
            return a
        if int(x) > b:
            return b
        return int(x)
        
def rgb_to_cmyk(r, g, b):
    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255
    k = 1 - max(r_norm, g_norm, b_norm)
    if k == 1:
        c = 0
        m = 0
        y = 0
    else:
        c = (1 - r_norm - k) / (1 - k)
        m = (1 - g_norm - k) / (1 - k)
        y = (1 - b_norm - k) / (1 - k)
    c = round(c * 100)
    m = round(m * 100)
    y = round(y * 100)
    k = round(k * 100)
    return c, m, y, k

def cmyk_to_rgb(c, m, y, k):
    c = c / 100
    m = m / 100
    y = y / 100
    k = k / 100
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    r = round(r)
    g = round(g)
    b = round(b)
    return r, g, b

def rgb_to_lab(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    def inv(c):
        if c > 0.04045:
            return ((c + 0.055) / 1.055) ** 2.4
        else:
            return c / 12.92
    r = inv(r)
    g = inv(g)
    b = inv(b)

    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047
    y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750) 
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883

    def f(t):
        if t > 0.008856:
            return t ** (1/3)
        else:
            return (7.787 * t) + (16 / 116)

    l = (116 * f(y)) - 16
    a = 500 * (f(x) - f(y))
    b = 200 * (f(y) - f(z))

    return round(l, 2), round(a, 2), round(b, 2)

def lab_to_rgb(l, a, b):
    def f_inv(t):
        if t > 0.2068966:
            return t ** 3
        else:
            return (t - 16 / 116) / 7.787

    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200
    x = 0.95047 * f_inv(x)
    y = 1.0 * f_inv(y)
    z = 1.08883 * f_inv(z)

    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    def cor(c):
        if c > 0.0031308:
            return 1.055 * (c ** (1 / 2.4)) - 0.055
        else:
            return 12.92 * c

    r = cor(r)
    g = cor(g)
    b = cor(b)

    r = min(max(0, r), 1) * 255
    g = min(max(0, g), 1) * 255
    b = min(max(0, b), 1) * 255

    return round(r), round(g), round(b)

class ColorConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Color Converter")
        self.geometry("470x600")
        self.resizable(False, False)

        self.rgb_label = ctk.CTkLabel(self, text="RGB")
        self.rgb_label.grid(row=0, column=0, padx=10, pady=10)

        self.r_entry = ctk.CTkEntry(self, placeholder_text="R: 0-255", width=80)
        self.r_entry.grid(row=0, column=2, padx=10, pady=10)
        self.r_entry.bind("<Return>", self.update_from_rgb)

        self.g_entry = ctk.CTkEntry(self, placeholder_text="G: 0-255", width=80)
        self.g_entry.grid(row=0, column=4, padx=10, pady=10)
        self.g_entry.bind("<Return>", self.update_from_rgb)

        self.b_entry = ctk.CTkEntry(self, placeholder_text="B: 0-255", width=80)
        self.b_entry.grid(row=0, column=6, padx=10, pady=10)
        self.b_entry.bind("<Return>", self.update_from_rgb)

        self.cmyk_label = ctk.CTkLabel(self, text="CMYK")
        self.cmyk_label.grid(row=1, column=0, padx=10, pady=10)

        self.c_entry = ctk.CTkEntry(self, placeholder_text="C: 0-100", width=80)
        self.c_entry.grid(row=1, column=2, padx=10, pady=10)
        self.c_entry.bind("<Return>", self.update_from_cmyk)

        self.m_entry = ctk.CTkEntry(self, placeholder_text="M: 0-100", width=80)
        self.m_entry.grid(row=1, column=4, padx=10, pady=10)
        self.m_entry.bind("<Return>", self.update_from_cmyk)

        self.y_entry = ctk.CTkEntry(self, placeholder_text="Y: 0-100", width=80)
        self.y_entry.grid(row=1, column=6, padx=10, pady=10)
        self.y_entry.bind("<Return>", self.update_from_cmyk)

        self.k_entry = ctk.CTkEntry(self, placeholder_text="K: 0-100", width=80)
        self.k_entry.grid(row=1, column=8, padx=10, pady=10)
        self.k_entry.bind("<Return>", self.update_from_cmyk)

        self.lab_label = ctk.CTkLabel(self, text="LAB")
        self.lab_label.grid(row=2, column=0, padx=10, pady=10)

        self.l_entry = ctk.CTkEntry(self, placeholder_text="L: 0-100", width=80)
        self.l_entry.grid(row=2, column=2, padx=10, pady=10)
        self.l_entry.bind("<Return>", self.update_from_lab)

        self.a_entry = ctk.CTkEntry(self, placeholder_text="A: -128-128", width=80)
        self.a_entry.grid(row=2, column=4, padx=10, pady=10)
        self.a_entry.bind("<Return>", self.update_from_lab)

        self.b_lab_entry = ctk.CTkEntry(self, placeholder_text="B: -128-128", width=80)
        self.b_lab_entry.grid(row=2, column=6, padx=10, pady=10)
        self.b_lab_entry.bind("<Return>", self.update_from_lab)

        self.colorpicker = CTkColorPicker(self, width=300, command=lambda e: self.choose_color(e))
        self.colorpicker.grid(row = 5, column = 0, columnspan=9, padx=10, pady=10)

        self.canvas = Canvas(self, width=300, height=100, highlightthickness=0)
        self.canvas.grid(row=4, column=2, columnspan=5, padx=10, pady=10)
        self.color_rect = self.canvas.create_rectangle(0, 0, 300, 100, fill="white")

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=6, column=0, columnspan=9, padx=10, pady=10)

        
    def update_error(self, message):
        self.error_label.configure(text=message)

    def update_from_rgb(self, event = None):
        r = entry_validator(0, 255, self.r_entry)
        g = entry_validator(0, 255, self.g_entry)
        b_rgb = entry_validator(0, 255, self.b_entry)
        self.r_entry.delete(0, ctk.END)
        self.r_entry.insert(0, str(r))
        self.g_entry.delete(0, ctk.END)
        self.g_entry.insert(0, str(g))
        self.b_entry.delete(0, ctk.END)
        self.b_entry.insert(0, str(b_rgb))    
        c, m, y, k = rgb_to_cmyk(r, g, b_rgb)
        l, a, b_lab = rgb_to_lab(r, g, b_rgb)
        self.canvas.itemconfig(self.color_rect, fill=rgb_to_hex(r, g, b_rgb))
        if (r, g, b_rgb) != cmyk_to_rgb(c, m, y, k) or (r, g, b_rgb) != lab_to_rgb(l, a, b_lab):
            self.update_error("Обнаружена потеря цвета")
        else:
            self.update_error("")

        self.c_entry.delete(0, ctk.END)
        self.c_entry.insert(0, str(c))
        self.m_entry.delete(0, ctk.END)
        self.m_entry.insert(0, str(m))
        self.y_entry.delete(0, ctk.END)
        self.y_entry.insert(0, str(y))
        self.k_entry.delete(0, ctk.END)
        self.k_entry.insert(0, str(k))

        self.l_entry.delete(0, ctk.END)
        self.l_entry.insert(0, str(l))
        self.a_entry.delete(0, ctk.END)
        self.a_entry.insert(0, str(a))
        self.b_lab_entry.delete(0, ctk.END)
        self.b_lab_entry.insert(0, str(b_lab))

    def update_from_cmyk(self, event = None):
        c = entry_validator(0, 100, self.c_entry)
        m = entry_validator(0, 100, self.m_entry)
        y = entry_validator(0, 100, self.y_entry)
        k = entry_validator(0, 100, self.k_entry)
        self.c_entry.delete(0, ctk.END)
        self.c_entry.insert(0, str(c))
        self.m_entry.delete(0, ctk.END)
        self.m_entry.insert(0, str(m))
        self.y_entry.delete(0, ctk.END)
        self.y_entry.insert(0, str(y))
        self.k_entry.delete(0, ctk.END)
        self.k_entry.insert(0, str(k))
        r, g, b_rgb = cmyk_to_rgb(c, m, y, k)
        l, a, b_lab = rgb_to_lab(r, g, b_rgb)
        self.canvas.itemconfig(self.color_rect, fill=rgb_to_hex(r, g, b_rgb))
        if (c, m, y, k) != rgb_to_cmyk(r, g, b_rgb) or (c, m, y, k) != rgb_to_cmyk(lab_to_rgb(l, a, b_lab)):
            self.update_error("Обнаружена потеря цвета")
        else:
            self.update_error("")

        self.r_entry.delete(0, ctk.END)
        self.r_entry.insert(0, str(r))
        self.g_entry.delete(0, ctk.END)
        self.g_entry.insert(0, str(g))
        self.b_entry.delete(0, ctk.END)
        self.b_entry.insert(0, str(b_rgb))

        self.l_entry.delete(0, ctk.END)
        self.l_entry.insert(0, str(l))
        self.a_entry.delete(0, ctk.END)
        self.a_entry.insert(0, str(a))
        self.b_lab_entry.delete(0, ctk.END)
        self.b_lab_entry.insert(0, str(b_lab))

    def update_from_lab(self, event = None):
        l = entry_validator(0, 100, self.l_entry)
        a = entry_validator(-128, 127, self.a_entry)
        b_lab = entry_validator(-128, 127, self.b_lab_entry)
        self.l_entry.delete(0, ctk.END)
        self.l_entry.insert(0, str(l))
        self.a_entry.delete(0, ctk.END)
        self.a_entry.insert(0, str(a))
        self.b_lab_entry.delete(0, ctk.END)
        self.b_lab_entry.insert(0, str(b_lab))
        r, g, b_rgb = lab_to_rgb(l, a, b_lab)
        c, m, y, k = rgb_to_cmyk(r, g, b_rgb)
        self.canvas.itemconfig(self.color_rect, fill=rgb_to_hex(r, g, b_rgb))
        if (l, a, b_lab) != rgb_to_lab(r, g, b_rgb) or (l, a, b_lab) != rgb_to_lab(*cmyk_to_rgb(c, m, y, k)):
            self.update_error("Обнаружена потеря цвета")
        else:
            self.update_error("")

        self.r_entry.delete(0, ctk.END)
        self.r_entry.insert(0, str(r))
        self.g_entry.delete(0, ctk.END)
        self.g_entry.insert(0, str(g))
        self.b_entry.delete(0, ctk.END)
        self.b_entry.insert(0, str(b_rgb))

        self.c_entry.delete(0, ctk.END)
        self.c_entry.insert(0, str(c))
        self.m_entry.delete(0, ctk.END)
        self.m_entry.insert(0, str(m))
        self.y_entry.delete(0, ctk.END)
        self.y_entry.insert(0, str(y))
        self.k_entry.delete(0, ctk.END)
        self.k_entry.insert(0, str(k))

    def choose_color(self, e):
        if e:
            r, g, b_rgb = hex_to_rgb(e)
            self.r_entry.delete(0, ctk.END)
            self.r_entry.insert(0, str(r))
            self.g_entry.delete(0, ctk.END)
            self.g_entry.insert(0, str(g))
            self.b_entry.delete(0, ctk.END)
            self.b_entry.insert(0, str(b_rgb))
            self.update_from_rgb()

if __name__ == "__main__":
    app = ColorConverterApp()
    app.mainloop()
