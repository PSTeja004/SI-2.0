import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class MainWindow(tk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        self.setup_ui()

    def set_data(self, data):
        self.data = data
        self.color_map()

    def setup_ui(self):
        self.min_temp = 16
        self.max_temp = 42

        self.button1 = tk.Button(self, text="Update", command=self.update_temp)
        self.button1.grid(row=0, column=0, padx=5, pady=5)

        self.color_bar_canvas = tk.Canvas(self, width=200, height=20)
        self.color_bar_canvas.grid(row=0, column=1,  padx=10, pady=10)

        self.min_temp_label = tk.Label(self, text="Min Temp:")
        self.min_temp_label.grid(row=1, column=0, padx=10, pady=10)

        self.min_temp_scale = tk.Scale(self, from_=self.min_temp, to=self.max_temp, orient="horizontal", resolution=0.08, length=200, command=self.update_min_temp)
        self.min_temp_scale.set(self.min_temp)
        self.min_temp_scale.grid(row=1, column=1, padx=10, pady=10)

        self.max_temp_label = tk.Label(self, text="Max Temp:")
        self.max_temp_label.grid(row=2, column=0, padx=10, pady=10)

        self.max_temp_scale = tk.Scale(self, from_=self.min_temp, to=self.max_temp, orient="horizontal", resolution=0.08,length=200, command=self.update_max_temp)
        self.max_temp_scale.set(self.max_temp)
        self.max_temp_scale.grid(row=2, column=1, padx=10, pady=10)

    def update_temp(self):
        self.min_temp=16
        self.max_temp=42
        self.min_temp_scale.set(self.min_temp)
        self.max_temp_scale.set(self.max_temp)
        self.color_map()
        
    def update_min_temp(self, value):
        new_val = float(value)
        if new_val >= self.max_temp:
            self.min_temp_scale.set(self.max_temp)
        self.min_temp = new_val
        self.color_map()

    def update_max_temp(self, value):
        new_val = float(value)
        if new_val <= self.min_temp:
            self.max_temp_scale.set(self.min_temp)
        self.max_temp = new_val
        self.color_map()

    def color_map(self):
        self.update_colorbar()
        if self.data is None or len(self.data) == 0:
            print("Data is None or empty")
            return None
        else:
            self.update_colorbar()
            normalized_data = (self.data - self.min_temp) / (self.max_temp - self.min_temp)
            colormap = plt.get_cmap('jet')
            rgba_data = colormap(normalized_data)
            pil_image = Image.fromarray((rgba_data * 255).astype(np.uint8))
            return pil_image
        
    def display(self):
        pass

    def update_colorbar(self):
        self.color_bar_canvas.delete("color")
        slider_blue_val = self.min_temp_scale.get()
        slider_red_val = self.max_temp_scale.get()

        # Calculate the width of the colored portion of the color bar
        color_width_blue = min((slider_blue_val - 16) * 10, 410)
        color_width_red = min((slider_red_val - 16) * 10, 410)

        # Draw the blue and red colored rectangles
        self.color_bar_canvas.create_rectangle(0, 0, color_width_blue, 20, fill="blue", outline="", tags="color")
        self.color_bar_canvas.create_rectangle(color_width_blue, 0, 410, 20, fill="red", outline="", tags="color")

        # Draw the black rectangle in the middle
        if slider_blue_val < slider_red_val:
            black_width = color_width_red - color_width_blue
            self.color_bar_canvas.create_rectangle(color_width_blue, 0, color_width_blue + black_width, 20, fill="black", outline="", tags="color")

    def get_inputs(self):
        return ['Thermal','Image','Video']

    def get_outputs(self):
        return ['Image']
    
    def get_data(self):
        if self.data is not None:
            pil_image = self.color_map()
            return pil_image
        else:
            return None
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Thermal Visualizer")
    result_window = MainWindow(root)
    result_window.pack(side=tk.TOP, padx=10, pady=10)
    root.mainloop()