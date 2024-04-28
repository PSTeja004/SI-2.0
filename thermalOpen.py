import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.file_directory = ""
        self.file_prefix = ""
        self.total_frames = 0
        self.frame_index = 0
        self.playing = False
        self.width = 0
        self.height = 0
        self.data=None
    
        self.label1 = tk.Label(self, text="Thermal File:")
        self.label1.grid(row=0, column=0)

        self.entry1 = tk.Entry(self, width=30)
        self.entry1.grid(row=0, column=1)

        self.button1 = tk.Button(self, text="Open", command=self.open_file)
        self.button1.grid(row=0, column=2)

        self.label2 = tk.Label(self, text="Total Frames:")
        self.label2.grid(row=1, column=0)

        self.entry2 = tk.Entry(self, state="readonly")
        self.entry2.grid(row=1, column=1)

        self.label3 = tk.Label(self, text="Frame Number:")
        self.label3.grid(row=2, column=0)

        self.entry3 = tk.Entry(self, state="readonly")
        self.entry3.grid(row=2, column=1)

        self.prev_button = tk.Button(self, text="Previous", command=self.prev_frame)
        self.prev_button.grid(row=3, column=0)

        self.play_button = tk.Button(self, text="Play/Pause", command=self.play_pause)
        self.play_button.grid(row=3, column=1)

        self.next_button = tk.Button(self, text="Next", command=self.next_frame)
        self.next_button.grid(row=3, column=2)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop)
        self.stop_button.grid(row=4, column=0)

        self.horizontal_slider = tk.Scale(self, from_=0, to=100, orient="horizontal", command=self.slider_callback, length=300)
        self.horizontal_slider.grid(row=4, column=1)

    def open_file(self):
        filename = filedialog.askopenfilename(title="Select Thermal File", filetypes=(("Text files", "*.txt"),))
        if filename:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, filename)
            self.file_directory = os.path.dirname(filename)
            self.file_prefix = os.path.splitext(os.path.basename(filename))[0][:-1]
            self.total_frames = self.get_total_frames()
            self.entry2.config(state="normal")
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, str(self.total_frames))
            self.entry2.config(state="readonly")
            self.horizontal_slider.set(0)
            self.frame_index = 0
            self.data=[]
            with open(filename, 'r') as file:
                content=file.readlines()
            
            self.height=int(content[0])
            self.width=int(content[1])

            for line in content[2:]:
                self.data.extend([float(val) for val in line.split()])

            # Convert array to numpy array
            self.data = np.array(self.data)

            # Reshape the data as per the frame size (assuming 640x512 here)
            self.data = self.data.reshape(self.width, self.height)

            self.next_frames()

            self.current_frame_data(self.data)

    def display(self):
        pass
       
    def next_frames(self):
        filename = os.path.join(self.file_directory, f"{self.file_prefix}{self.frame_index}.txt")
        with open(filename, 'r') as file:
            content=file.readlines()
        self.data=[]
            
        self.height=int(content[0])
        self.width=int(content[1])

        for line in content[2:]:
            self.data.extend([float(val) for val in line.split()])

        # Convert array to numpy array
        self.data = np.array(self.data)

        # Reshape the data as per the frame size (assuming 640x512 here)
        self.data = self.data.reshape(self.width, self.height)

        self.current_frame_data(self.data)

    def current_frame_data(self,frame_data):
        return frame_data

    def get_total_frames(self):
        frame_number = 0
        while True:
            filename = os.path.join(self.file_directory, f"{self.file_prefix}{frame_number}.txt")
            if not os.path.exists(filename):
                break
            frame_number += 1
        return frame_number
    
    def play_pause(self):
        if self.playing:
            self.playing = False
        else:
            self.playing = True
            self.play_frames()

    def play_frames(self):
        #delay=100
        while self.playing and self.frame_index < self.total_frames:
            self.frame_index += 1
            if self.entry3.winfo_exists():
                self.entry3.config(state="normal")
                self.entry3.delete(0, tk.END)
                self.entry3.insert(0, str(self.frame_index))
                self.entry3.config(state="readonly")
            if self.horizontal_slider.winfo_exists():
                self.horizontal_slider.set((self.frame_index / self.total_frames) * 100)
            self.update()
        #    self.after(delay)
            self.next_frames()

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
            self.update_frame_entry()
            self.next_frames()

    def update_frame_entry(self):
        self.entry3.config(state="normal")
        self.entry3.delete(0, tk.END)
        self.entry3.insert(0, str(self.frame_index))
        self.entry3.config(state="readonly")

    def next_frame(self):
        if self.frame_index < self.total_frames - 1:
            self.frame_index += 1
            self.next_frames()

    def slider_callback(self, value):
        self.frame_index = int((int(value) / 100) * self.total_frames)
        self.next_frames()
        
    def get_inputs(self):
        return []
    
    def get_outputs(self):
        return ['Thermal']
    
    def get_data(self):
        return self.data
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Thermal Open")

    main_window = MainWindow(root)
    main_window.pack(side=tk.TOP, padx=10, pady=10)

    root.mainloop()
