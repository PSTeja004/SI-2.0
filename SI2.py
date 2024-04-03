import tkinter as tk
from tkinter import ttk, messagebox
import os
import importlib.util
line=None

class ResultWindows(tk.Frame):
    inputLabels=[]
    outputLabels=[]
    def __init__(self, parent, inputLabels,outputLabels):
        super().__init__(parent)
        self.parent = parent
        self.inputLabels = inputLabels
        self.outputLabels = outputLabels

        self.canvas = tk.Canvas(parent,width=200,height=200, background='lightblue')
        self.canvas.pack()

        button_width = 20  
        button_height = 20
        padding_y=30

        for i in range(len(self.inputLabels)):
            self.button_frame = tk.Frame(self.canvas, width=button_width, height=button_height, 
                         bg="green", highlightthickness=2, highlightbackground="blue")
            self.button_window = self.canvas.create_window(5, (button_height+(padding_y*i)),anchor='nw', window=self.button_frame)
            self.lable = self.canvas.create_text(button_width+10,(button_height+(padding_y*i)),anchor='nw', text=self.inputLabels[i], font=("Arial", 16), fill='black')

        for i in range(len(self.outputLabels)):
            self.button_frame = tk.Frame(self.canvas, width=button_width, height=button_height, 
                         bg="red", highlightthickness=2, highlightbackground="blue")
            self.button_window = self.canvas.create_window(180, (button_height+(padding_y*i)),anchor='nw', window=self.button_frame)
            self.lable = self.canvas.create_text(120,(button_height+(padding_y*i)),anchor='nw', text=self.outputLabels[i], font=("Arial", 16), fill='black')

class DragManager():
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.active_widget = None

    def add_draggable(self, widget):
        widget.bind("<ButtonPress-1>", lambda event, widget=widget: self.on_drag_start(event, widget))
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor='hand1')

    def on_drag_start(self, event, widget):
        self.active_widget = widget
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_drag(self, event):
        if self.active_widget:
            delta_x = event.x_root - self.start_x
            delta_y = event.y_root - self.start_y
            x = self.active_widget.winfo_x() + delta_x
            y = self.active_widget.winfo_y() + delta_y
            self.active_widget.place(x=x, y=y)
            self.start_x = event.x_root
            self.start_y = event.y_root

    def on_drop(self, event):
        self.active_widget = None
        return True

class Canvas_Manager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.links = []
        self.current_link = None
        self.bind_events()

    def bind_events(self):
        self.canvas.bind("<Double-Button-1>", self.start_link)
        self.canvas.bind("<B1-Motion>", self.draw_link)
        self.canvas.bind("<ButtonRelease-1>", self.end_link)

    def start_link(self, event):
        self.current_link = [event.x, event.y]

    def draw_link(self, event):
        if self.current_link:
            self.canvas.delete("link")
            self.canvas.create_line(self.current_link[0], self.current_link[1], event.x, event.y, tag="link", fill="red", width=2)

    def end_link(self, event):
        self.current_link = None
        
class Ui_MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MainWindow")
        self.root.geometry("800x600")

        self.tabWidget = ttk.Notebook(self.root)
        self.tabWidget.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(self.tabWidget)
        self.tabWidget.add(self.tab1, text="Plugin Graph")

        self.groupBox1 = ttk.LabelFrame(self.tab1, text="Create Configuration")
        self.groupBox1.pack(side="top", anchor="nw", padx=10, pady=10)

        self.pushButton_2 = ttk.Button(self.groupBox1, text="New",command=self.clear_frames)
        self.pushButton_2.pack(side="left")

        # Combobox to display pyc files
        self.comboBox = ttk.Combobox(self.groupBox1)
        self.comboBox.pack(side="left")


        self.groupBox2 = ttk.LabelFrame(self.tab1, text="Load/Save Configuration")
        self.groupBox2.pack(side="top", anchor="nw", padx=10, pady=10)

        self.comboBox_2 = ttk.Combobox(self.groupBox2)
        self.comboBox_2.pack(side="left")

        self.pushButton_3 = ttk.Button(self.groupBox2, text="Save")
        self.pushButton_3.pack(side="left")

        self.groupBox3 = tk.LabelFrame(self.tab1, text="PluginGroupBox")
        self.groupBox3.pack(side="top", anchor="nw", padx=10, pady=10, fill="both", expand=True)

        # Create a canvas inside the groupbox
        self.canvas = tk.Canvas(self.groupBox3, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tab2 = ttk.Frame(self.tabWidget)
        self.tabWidget.add(self.tab2, text="User Interface")

        self.groupBox4 = tk.LabelFrame(self.tab2, text="UIGroupBox")
        self.groupBox4.pack(side="top", anchor="nw", padx=10, pady=10, fill="both", expand=True)

        self.pushButton_4 = ttk.Button(self.tab2, text="Start")
        self.pushButton_4.pack(side="left", padx=10, pady=10)  # Adjusted position

        self.pushButton_5 = ttk.Button(self.tab2, text="Hide All Doc Pins")
        self.pushButton_5.pack(side="left", padx=10, pady=10)  # Adjusted position

        self.pushButton = ttk.Button(self.root, text="Exit", command=self.exit_application)
        self.pushButton.pack(side="bottom", anchor="se", padx=10, pady=10)  # Anchor to bottom-right corner

        self.tabWidget.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.comboBox.bind("<<ComboboxSelected>>", self.load_selected_file)

        # list to keep tracks of frames added
        self.frames_groupbox3 = []
        self.frames_groupbox4 = []

        # Container frame for draggable frames
        self.container_frame4 = tk.Frame(self.groupBox4)
        self.container_frame4.pack(fill="both", expand=True)

        # Create a single instance of DragManager
        self.drag_manager = DragManager()
        self.canvas_manager = Canvas_Manager(self.canvas)

        # Populate Combobox with DLL files
        self.populate_pyc_files()
    
    def populate_pyc_files(self):
        # Get the current directory
        current_directory = os.getcwd()
        # List all files in the directory
        pyc_files = [file for file in os.listdir(current_directory) if file.endswith(".py")]
        # Populate Combobox with PYC file names
        self.comboBox["values"] = pyc_files

    def on_tab_change(self, event):
        current_tab = self.tabWidget.select()
        tab_text = self.tabWidget.tab(current_tab, "text")
        if tab_text == "User Interface":
            self.root.title("User Interface Tab")
        elif tab_text == "Plugin Graph":
            self.root.title("Plugin Graph Tab")

    def clear_frames(self):
        # Destroy frames in groupBox3
        for frame in self.frames_groupbox3:
            frame.destroy()
        # Clear the list
        self.frames_groupbox3 = []

        # Destroy frames in groupBox4
        for frame in self.frames_groupbox4:
            frame.destroy()
        # Clear the list
        self.frames_groupbox4 = []

    def load_selected_file(self, event=None):
        # Create a new frame
        frame4 = ttk.Frame(self.container_frame4, relief="solid", borderwidth=5)
        frame4.pack(side="left", padx=10)
        self.frames_groupbox4.append(frame4)  # Store reference to the frame

        # Create a new frame
        frame3 = tk.Canvas(self.canvas, relief="solid", borderwidth=5)
        frame3.pack(side="left", padx=10)
        self.frames_groupbox3.append(frame3)  # Store reference to the frame


        # Make the frame draggable
        self.drag_manager.add_draggable(frame4)
        self.drag_manager.add_draggable(frame3)

        #Call canvas events to establish visual connection
        self.canvas_manager.bind_events()

        selected_file = self.comboBox.get()
        print(selected_file)
        if selected_file:
            try:
                module_name = os.path.splitext(selected_file)[0]
                module_path = os.path.join(os.getcwd(), selected_file)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                main_window = module.MainWindow(frame4)
                main_window.pack(fill="both", expand=True)

                inputs = main_window.get_inputs()
                outputs = main_window.get_outputs()

                result_window = ResultWindows(frame3,inputLabels=inputs, outputLabels=outputs)
                result_window.pack(fill="both", expand=True)

                close_button = ttk.Button(frame3, text="Close", command=lambda: (frame4.destroy(), frame3.destroy()))
                close_button.pack(side="bottom")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
            

    def exit_application(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ui = Ui_MainWindow(root)
    root.mainloop()
