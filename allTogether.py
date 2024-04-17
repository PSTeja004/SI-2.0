import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors

class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.file_directory = ""
        self.file_prefix = ""
        self.total_frames = 0
        self.frame_index = 0
        self.playing = False

        self.setup_ui()

    def setup_ui(self):
        self.label1 = tk.Label(self, text="Thermal File:")
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.entry1 = tk.Entry(self, width=50)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        self.button1 = tk.Button(self, text="Open", command=self.open_file)
        self.button1.grid(row=0, column=2, padx=10, pady=10)

        self.label2 = tk.Label(self, text="Total Frames:")
        self.label2.grid(row=1, column=0, padx=10, pady=10)

        self.entry2 = tk.Entry(self, state="readonly")
        self.entry2.grid(row=1, column=1, padx=10, pady=10)

        self.label3 = tk.Label(self, text="Frame Number:")
        self.label3.grid(row=5, column=0, padx=10, pady=10)

        self.entry3 = tk.Entry(self, state="readonly")
        self.entry3.grid(row=5, column=1, padx=10, pady=10)

        self.min_temp = 25  # default min temp value, adjust as needed
        self.max_temp = 34  # default max temp value, adjust as needed

        self.min_temp_label = tk.Label(self, text="Min Temp:")
        self.min_temp_label.grid(row=6, column=0, padx=10, pady=10)

        self.min_temp_scale = tk.Scale(self, from_=16, to=42, orient="horizontal", resolution=0.08, command=self.update_min_temp, length=300)
        self.min_temp_scale.set(self.min_temp)
        self.min_temp_scale.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

        self.max_temp_label = tk.Label(self, text="Max Temp:")
        self.max_temp_label.grid(row=7, column=0, padx=10, pady=10)

        self.max_temp_scale = tk.Scale(self, from_=16, to=42, orient="horizontal", resolution=0.08, command=self.update_max_temp, length=300)
        self.max_temp_scale.set(self.max_temp)
        self.max_temp_scale.grid(row=7, column=1, columnspan=2, padx=10, pady=10)


        self.prev_button = tk.Button(self, text="Previous", command=self.prev_frame)
        self.prev_button.grid(row=8, column=0, padx=10, pady=10)

        self.play_button = tk.Button(self, text="Play/Pause", command=self.play_pause)
        self.play_button.grid(row=8, column=1, padx=10, pady=10)

        self.next_button = tk.Button(self, text="Next", command=self.next_frame)
        self.next_button.grid(row=8, column=2, padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop)
        self.stop_button.grid(row=8, column=3, padx=10, pady=10)

        self.graphical_viewer = tk.Label(self)
        self.graphical_viewer.grid(row=0, column=4, rowspan=9, padx=10, pady=10)

        self.horizontal_slider = tk.Scale(self, from_=0, to=100, orient="vertical", command=self.slider_callback, length=300)
        self.horizontal_slider.grid(row=0, column=5, rowspan=9, padx=10, pady=10)


    def open_file(self):
        filename = filedialog.askopenfilename(title="Select Thermal File", filetypes=(("Text files", "*.txt"),))
        if filename:
            self.entry1.delete(0, tk.END)  # Clear any previous content
            self.entry1.insert(0, filename)  # Insert the path of the selected file
            self.file_directory = os.path.dirname(filename)
            self.file_prefix = os.path.splitext(os.path.basename(filename))[0][:-1]
            self.total_frames = self.get_total_frames()
            self.entry2.config(state="normal")
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, str(self.total_frames))
            self.entry2.config(state="readonly")
            self.horizontal_slider.set(0)
            self.frame_index = 0
            self.display_frame()

    def get_total_frames(self):
        frame_number = 0
        while True:
            filename = os.path.join(self.file_directory, f"{self.file_prefix}{frame_number}.txt")
            if not os.path.exists(filename):
                break
            frame_number += 1
        return frame_number
    
    def update_min_temp(self, value):
        self.min_temp = float(value)
        self.display_frame()

    def update_max_temp(self, value):
        self.max_temp = float(value)
        self.display_frame()

    def play_pause(self):
        if self.playing:
            self.playing = False
        else:
            self.playing = True
            self.play_frames()

    def play_frames(self):
        while self.playing and self.frame_index < self.total_frames:
            self.display_frame()
            self.frame_index += 1
            self.entry3.config(state="normal")
            self.entry3.delete(0, tk.END)
            self.entry3.insert(0, str(self.frame_index))
            self.entry3.config(state="readonly")
            self.horizontal_slider.set((self.frame_index / self.total_frames) * 100)
            self.update()

    def stop(self):
        self.playing = False
        self.frame_index = 0
        self.entry3.config(state="normal")
        self.entry3.delete(0, tk.END)
        self.entry3.insert(0, "0")
        self.entry3.config(state="readonly")
        self.horizontal_slider.set(0)

    def prev_frame(self):
        if self.frame_index > 0:
            self.frame_index -= 1
            self.display_frame()

    def next_frame(self):
        if self.frame_index < self.total_frames - 1:
            self.frame_index += 1
            self.display_frame()

    def slider_callback(self, value):
        self.frame_index = int((int(value) / 100) * self.total_frames)
        self.display_frame()

    
    def display_frame(self):
        filename = os.path.join(self.file_directory, f"{self.file_prefix}{self.frame_index}.txt")
        # Read content of the file
        with open(filename, 'r') as file:
            content = file.readlines()

        # Parse content into array
        data = []
        for line in content[2:]:
            data.extend([float(val) for val in line.split()])

        # Convert array to numpy array
        data = np.array(data)

        # Reshape the data as per the frame size (assuming 640x512 here)
        data = data.reshape(512, 640)

        # Normalize the data between the selected min and max temperature values
        norm = mcolors.Normalize(vmin=self.min_temp, vmax=self.max_temp)

        # Apply the colormap to the normalized data to get an RGBA image
        #rgba_image = plt.cm.jet(norm(data))
        rgba_image = plt.cm.jet_r(norm(data))

        # Display the RGBA image
        plt.imshow(rgba_image, interpolation='nearest')
        plt.axis('off')  # Turn off axis
        plt.savefig('temp.png')  # Save as temp.png
        plt.close()  # Close plot to avoid showing multiple plots
        photo = tk.PhotoImage(file='temp.png')  # Load the image
        self.graphical_viewer.config(image=photo)  # Update the image
        self.graphical_viewer.image = photo  # Keep a reference
        os.remove('temp.png')  # Remove the temporary image file

    def get_inputs(self):
        return []
    
    def get_outputs(self):
        return []


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Thermal File")
    app = MainWindow(root)
    app.pack(side=tk.TOP, padx=10, pady=10)
    root.mainloop()