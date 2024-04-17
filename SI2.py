from tkinter import ttk, messagebox
import tkinter as tk
import os
import importlib.util

line = None
class ResultWindows(tk.Canvas):
    def __init__(self, parent, ui_main_window=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ui_main_window = ui_main_window
        self.config(bg='white')
        self.lst=[]
        self.plugin_horizontal_gap = 250
        self.input_output_gap = 150
        self.plugins = []
        self.temp_line = None
        self.link_start = None
        self.link_end = None
        self.selected_input = None
        self.selected_output = None
        self.connections = []  # Stores connection data
        
    def add_plugin(self, inputLabels, outputLabels, plugin_name):
        start_x = 10 + len(self.plugins) * self.plugin_horizontal_gap if self.plugins else 10
        start_y, button_width, button_height, text_padding = 10, 20, 20, 5
        
        input_start_x = start_x
        output_start_x = start_x + self.input_output_gap
        
        self.create_text(start_x + self.input_output_gap / 2, start_y, text=plugin_name, font=("Arial", 14, "bold"), fill="blue", tags="plugin")
        
        for i, label in enumerate(inputLabels):
            input_y = start_y + 20 + (i * (button_height + 10))
            input_btn = self.create_rectangle(input_start_x, input_y, input_start_x + button_width, input_y + button_height, fill="green", tags=("input", f"input_{plugin_name}_{i}"))
            self.create_text(input_start_x + button_width + text_padding * 2, input_y + button_height / 2, text=label, anchor="w", font=("Arial", 12), fill="blue", tags="plugin")
            self.tag_bind(input_btn, "<ButtonPress>", lambda event, name=f"{plugin_name}": self.finalize_link(event, name=name))
        
        for i, label in enumerate(outputLabels):
            output_y = start_y + 20 + (i * (button_height + 10))
            output_btn = self.create_rectangle(output_start_x, output_y, output_start_x + button_width, output_y + button_height, fill="red", tags=("output", f"output_{plugin_name}_{i}"))
            self.create_text(output_start_x - text_padding * 2, output_y + button_height / 2, text=label, anchor="e", font=("Arial", 12),fill="blue", tags="plugin")
            self.tag_bind(output_btn, "<ButtonPress-1>", lambda event, name=f"{plugin_name}": self.start_link(event, name=name))
        
        self.plugins.append(plugin_name)

    def start_link(self, event, name):
        self.link_start = (event.x, event.y)
        print("link started",name)
        self.lst.append(name)
        # Create a temporary line if desired
        self.temp_line = self.create_line(self.link_start[0], self.link_start[1], event.x, event.y, fill="blue", dash=(4, 2))
        self.connections.append({'start': name, 'type': 'left-click'})

    def finalize_link(self, event, name):
        if ((event.num == 2) | (event.num == 3)):
            if self.temp_line and self.link_start:
                # Draw the final line
                self.create_line(self.link_start[0], self.link_start[1], event.x, event.y, fill="red", width=2)
                print('link finished',name)
                self.lst.append(name)
                # Cleanup
                self.connections.append({'end': name, 'type': 'right-click'})
                self.delete(self.temp_line)
                self.temp_line = None
                self.link_start = None

    def clear_plugins(self):
        # Print debug info to confirm the method is being called
        print("Clearing all plugins from the canvas")

        # Remove all items from the canvas to ensure no items are left undeleted
        self.delete("all")

        # Clear temporary drawing states
        self.temp_line = None
        self.link_start = None
        self.link_end = None

        # Clear the plugins list and reset selection states
        self.plugins = []
        self.selected_input = None
        self.selected_output = None


    def update_link(self, event):
        if self.temp_line and self.link_start:
            # Update temporary line's end point to follow the mouse
            self.coords(self.temp_line, self.link_start[0], self.link_start[1], event.x, event.y)



    def reset_selection(self, input_or_output):
        # Reset the selection based on input_or_output argument
        if input_or_output == "output" and self.selected_output_tag:
            self.itemconfig(self.selected_output_tag, fill="red")  # Reset to default color
        elif input_or_output == "input" and self.selected_input_tag:
            self.itemconfig(self.selected_input_tag, fill="green")  # Reset to default color
                
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
        
    
    def on_canvas_right_click(self, event):
        item = self.find_closest(event.x, event.y)
        self.gettags(item)
        # Process tags to determine if an output button was clicked and handle accordingly

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
        self.processing = False  # State flag to track processing state

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

        self.canvas = ResultWindows(self.groupBox3)
        self.canvas = ResultWindows(self.groupBox3, ui_main_window=self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        

        self.tab2 = ttk.Frame(self.tabWidget)
        self.tabWidget.add(self.tab2, text="User Interface")

        self.groupBox4 = tk.LabelFrame(self.tab2, text="UIGroupBox")
        self.groupBox4.pack(side="top", anchor="nw", padx=10, pady=10, fill="both", expand=True)

        
        # Create a canvas inside the groupbox
        self.canvas1 = tk.Canvas(self.groupBox4, bg='white')
        self.canvas1.pack(fill=tk.BOTH, expand=True)

        self.pushButton_5 = ttk.Button(self.tab2, text="Hide All Doc Pins")
        self.pushButton_5.pack(side="left", padx=10, pady=10)  # Adjusted position

        self.pushButton = ttk.Button(self.root, text="Exit", command=self.exit_application)
        self.pushButton.pack(side="bottom", anchor="se", padx=10, pady=10)  # Anchor to bottom-right corner

        self.tabWidget.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.comboBox.bind("<<ComboboxSelected>>", self.load_selected_file)

        # list to keep tracks of frames added
        self.frames_groupbox3 = []
        self.frames_groupbox4 = []

        # Create a single instance of DragManager
        self.drag_manager = DragManager()
        self.canvas_manager = Canvas_Manager(self.canvas)

        self.plugin_instances = {}

        # Populate Combobox with DLL files
        self.populate_pyc_files()
        self.setup_ui()
        
    def setup_ui(self):
        # UI setup...
        self.pushButton_4 = ttk.Button(self.tab2, text="Start", command=self.toggle_process)
        self.pushButton_4.pack(side="left", padx=10, pady=10)

        
    def toggle_process(self):
        if self.processing:
            self.pushButton_4.config(text="Start")
            self.stop_processing()
        else:
            self.pushButton_4.config(text="Pause")
            self.start_processing()
        self.processing = not self.processing
    
    def start_processing(self):
        # Actual start processing logic
        print("Starting data flow...")
        for conn in self.canvas.connections:
            if conn['type'] == 'end':
                source_plugin = conn['start']
                target_plugin = conn['end']
                self.start_data_flow(source_plugin, target_plugin)

    def stop_processing(self):
        print("Processing stopped.")

    def populate_pyc_files(self):
        # Get the current directory
        current_directory = os.getcwd()
        # List all files in the directory
        pyc_files = [file for file in os.listdir(current_directory) if file.endswith(".py")]
        # Populate Combobox with PYC file names
        self.comboBox["values"] = pyc_files
        
    def start_data_flow(self, source, target):
        # Assuming both plugins are correctly configured and exist
        if source in self.plugin_instances and target in self.plugin_instances:
            processed_data = self.plugin_instances[source].process_file()
            self.plugin_instances[target].display_data(processed_data)
            print(f"Data processed from {source} to {target}")

    def on_tab_change(self, event):
        current_tab = self.tabWidget.select()
        tab_text = self.tabWidget.tab(current_tab, "text")
        if tab_text == "User Interface":
            self.root.title("User Interface Tab")
        elif tab_text == "Plugin Graph":
            self.root.title("Plugin Graph Tab")

    def clear_frames(self):
        print("Clearing frames and plugins from the UI")

        # Clear frames in groupBox3
        for frame in self.frames_groupbox3:
            frame.destroy()
        self.frames_groupbox3.clear()

        # Clear frames in groupBox4
        for frame in self.frames_groupbox4:
            frame.destroy()
        self.frames_groupbox4.clear()

        # Call clear_plugins to remove all plugins and related visual elements from the canvas
        self.canvas.clear_plugins()

    def update_ui_tab(self):
        # Clear existing content in the UI group box
        for widget in self.groupBox4.winfo_children():
            widget.destroy()

        # Add labels for each plugin configured
        for i, plugin_name in enumerate(self.pluginCanvas.plugins, start=1):
            tk.Label(self.groupBox4, text=f"Plugin {i}: {plugin_name}", font=("Arial", 12)).pack()

    def clear_plugins(self):
        self.canvas.clear_plugins()

    def load_selected_file(self, event=None):
        
        frame4 = tk.Frame(self.canvas1, relief="solid", borderwidth=5)
        frame4.pack(side="left", padx=10)
        self.frames_groupbox4.append(frame4)  # Store reference to the frame

        # Make the frame draggable
        self.drag_manager.add_draggable(frame4)


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

                self.plugin_instances[selected_file] = main_window  # Store plugin instance for use

                self.canvas.add_plugin(inputLabels=inputs, outputLabels=outputs,plugin_name=selected_file)

                print(self.plugin_instances)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
            

    def exit_application(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    ui = Ui_MainWindow(root)
    root.mainloop()