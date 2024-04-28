import tkinter as tk
from PIL import ImageTk

class MainWindow(tk.Frame):
    def __init__(self, parent, img=None):
        super().__init__(parent)
        self.parent = parent
        self.img = img
        self.setup_ui()

    def set_data(self, img):
        self.img = img
        self.display()

    def setup_ui(self):
        self.graphical_viewer = tk.Label(self)
        self.graphical_viewer.grid(row=0, column=0, padx=10, pady=10)
        self.display()

    def display(self):  
        if self.img is None:
            print("disply none.")
            return None
        else:     
            # Convert PIL image to Tkinter PhotoImage
            photo = ImageTk.PhotoImage(self.img)
            
            # Update the image in the graphical viewer
            self.graphical_viewer.config(image=photo)
            self.graphical_viewer.image = photo
            
            return None

    def get_inputs(self):
        return [['Image']]

    def get_outputs(self):
        return []
    
    def get_data(self):
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Display")
    root.geometry("800x600")
    result_window = MainWindow(root)
    result_window.pack(side=tk.TOP, padx=10, pady=10)
    root.mainloop()