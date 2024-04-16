import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors

class MainWindow(tk.Frame):
    def __init__(self, parent, img=None):
        super().__init__(parent)
        self.parent = parent
        self.img = img
        self.setup_ui()

    def setup_ui(self):
        self.graphical_viewer = tk.Label(self)
        self.graphical_viewer.grid(row=0, column=0, padx=10, pady=10)
        self.display()

    def display(self):  
        if self.img is None or len(self.img) == 0:
            print("Data is None or empty")
            return None
        else:     
            # Display the RGBA image
            plt.imshow(self.img, interpolation='nearest')
            plt.axis('off')  # Turn off axis
            plt.savefig('temp.png')  # Save as temp.png
            photo = tk.PhotoImage(file='temp.png')
            self.graphical_viewer.config(image=photo)  # Update the image
            self.graphical_viewer.image = photo
            os.remove('temp.png')

    def get_inputs(self):
        return [['Image']]

    def get_outputs(self):
        return []
    
    def get_data(self):
        return self.color_map()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Display")
    root.geometry("800x600")
    result_window = MainWindow(root)
    result_window.pack(side=tk.TOP, padx=10, pady=10)
    root.mainloop()