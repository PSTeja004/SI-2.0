# si2optmised - optimised Friday afternoon with settings as discussed.

from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import os
import importlib.util
import threading
import time

line = None
opened_files_instances={}
links_conn={}
start=[]
end=[]

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
        global start
        self.link_start = (event.x, event.y)
        self.lst.append(name)
        # Create a temporary line if desired
        self.temp_line = self.create_line(self.link_start[0], self.link_start[1], event.x, event.y, fill="blue", dash=(4, 2))
        self.connections.append({'start': name, 'type': 'start-link'})
        start.append(name)
    
    def create_custom_line(self, start_x, start_y, end_x, end_y, fill='red', width=2, tags=None):
        line_id = self.create_line(start_x, start_y, end_x, end_y, fill=fill, width=width, tags=tags)
        return line_id

    def finalize_link(self, event, name):
        global end
        if ((event.num == 2) | (event.num == 3)):
            if self.temp_line and self.link_start:
                # Draw the final line
                line_id = self.create_line(self.link_start[0], self.link_start[1], event.x, event.y, fill="black", width=2)
                self.lst.append(name)
                # Cleanup
                self.connections.append({'end': name, 'type': 'end-link', 'line_id': line_id})
                end.append(name)
                self.delete(self.temp_line)
                self.temp_line = None
                self.link_start = None

    def clear_plugins(self):
        # Print debug info to confirm the method is bei
        print("Clear plugins")

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

        self.pushButton_3 = ttk.Button(self.groupBox2, text="Save", command=self.save_configuration_dialog)
        self.pushButton_3.pack(side="left")

        self.pushButton_4 = ttk.Button(self.groupBox2, text="Load", command=self.load_configuration)
        self.pushButton_4.pack(side="right")

        self.tabWidget.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.comboBox.bind("<<ComboboxSelected>>", self.load_selected_file)

        # list to keep tracks of frames added
        self.frames_groupbox3 = []
        self.frames_groupbox4 = []

        # Create a single instance of DragManager
        self.drag_manager = DragManager()
        self.canvas_manager = Canvas_Manager(self.canvas)

        self.plugin_instances = {}
        self.processing_event = threading.Event()

        # Populate Combobox with DLL files
        self.populate_pyc_files()
        self.setup_ui()

        self.populate_saved_configurations()

        
    def setup_ui(self):
        # UI setup...
        self.pushButton_4 = ttk.Button(self.tab2, text="Start", command=self.toggle_process)
        self.pushButton_4.pack(side="left", padx=10, pady=10)

        
    def toggle_process(self):
        if self.processing:
            self.pushButton_4.config(text="Start")
            self.processing = False
            self.processing_event.clear()  # Clear the event to pause the thread
        else:
            self.pushButton_4.config(text="Pause")
            self.processing = True
            self.processing_event.set()  # Set the event to resume the thread
            self.start_processing()
    
    def start_processing(self):
        print("Starting data flow...")
        self.processing = True
        self.processing_thread = threading.Thread(target=self.process_all_links_loop)
        self.processing_thread.start()
    
    def process_all_links_loop(self):
        print('\nentering process_all_links_loop fucntion\n')
        global start, end, opened_files_instances

        '''while self.processing:
            if self.processing_event.is_set():
                # Loop through all connections and transfer data
                for link_index in range(len(start)):
                    start_plugin = start[link_index]
                    end_plugin = end[link_index]

                    # Retrieve data from the start plugin
                    data = opened_files_instances[start_plugin].get_data()

                    # Set data to the end plugin and update the end plugin instance
                    opened_files_instances[end_plugin].set_data(data)
                    #opened_files_instances[end_plugin].parent.update()  # Update the parent window to refresh the UI

            time.sleep(0.05)

        print("Processing stopped.")'''

        def update_ui():
            if self.processing_event.is_set():
                # Loop through all connections and transfer data
                for link_index in range(len(start)):
                    start_plugin = start[link_index]
                    end_plugin = end[link_index]

                    # Retrieve data from the start plugin
                    data = opened_files_instances[start_plugin].get_data()

                    # Set data to the end plugin and update the end plugin instance
                    opened_files_instances[end_plugin].set_data(data)

                    # Schedule the UI update in the main thread
                    opened_files_instances[end_plugin].parent.after(0, opened_files_instances[end_plugin].parent.update)

            # Repeat the update_ui function after a short delay
            self.root.after(50, update_ui)

        # Start the UI update loop
        update_ui()

        print("Processing stopped.")


    def stop_processing(self):
        print("Stopping data flow...")
        self.processing = False
        self.processing_event.clear()  # Clear the event to stop the thread
        if self.processing_thread.is_alive():
            self.processing_thread.join()



    def start_data_flow(self, links):
        global opened_files_instances
        # Assuming both plugins are correctly configured and exist
        for start,end in links.items():
            data = opened_files_instances[start].get_data()
            end_instance = opened_files_instances[end].set_data(data)
            if end_instance!=None:
                opened_files_instances[end] = end_instance

            

    def populate_pyc_files(self):
        # Get the current directory
        current_directory = os.getcwd()

        # Get the name of the current Python file
        current_file = os.path.basename(__file__)
        
        # List all Python files in the current directory
        pyc_files = [file for file in os.listdir(current_directory) if file.endswith(".py")]
        
        # Sort the list of Python files
        pyc_files.sort()
        
        # Exclude "SInterface2.py" from the list
        result_list = list(filter(lambda x: x != current_file, pyc_files))
        
        # Populate the Combobox with the list of Python files
        self.comboBox["values"] = result_list
        
    def on_tab_change(self, event):
        current_tab = self.tabWidget.select()
        tab_text = self.tabWidget.tab(current_tab, "text")
        if tab_text == "User Interface":
            self.root.title("User Interface Tab")
        elif tab_text == "Plugin Graph":
            self.root.title("Plugin Graph Tab")

    def clear_frames(self):
        global opened_files_instances
        global links_conn
        global start
        global end
        
        # Clear frames in groupBox3
        #for frame in self.frames_groupbox3:
        #    frame.destroy()
        self.frames_groupbox3.clear()

        # Clear frames in groupBox4
        for frame in self.frames_groupbox4:
            frame.destroy()
        self.frames_groupbox4.clear()
        
        # Clear canvas connections
        self.canvas.connections.clear()
        
        # Call clear_plugins to remove all plugins and related visual elements from the canvas
        self.canvas.clear_plugins()

        #clear global variable
        opened_files_instances.clear()
        links_conn.clear()
        start.clear()
        end.clear()


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
        global opened_files_instances

        frame4 = tk.Frame(self.canvas1, relief="solid", borderwidth=5)
        frame4.pack(side="left", padx=10)
        self.frames_groupbox4.append(frame4)  # Store reference to the frame

        # Make the frame draggable
        self.drag_manager.add_draggable(frame4)

        #Call canvas events to establish visual connection
        self.canvas_manager.bind_events()

        selected_file = self.comboBox.get()
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

                opened_files_instances[selected_file] = main_window

                self.plugin_instances[selected_file] = main_window  # Store plugin instance for use

                self.canvas.add_plugin(inputLabels=inputs, outputLabels=outputs, plugin_name=selected_file)

                # Store the plugin name in the frame
                frame4.plugin_name = selected_file
                self.frames_groupbox3.append(selected_file) 
                #frame3.plugin_name = selected_file


            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def save_configuration(self, file_path):
        config_folder = os.path.join(os.getcwd(), "config_new")
        os.makedirs(config_folder, exist_ok=True)
        file_name = os.path.basename(file_path)
        file_name = file_name.replace(".py", "_config.py")
        file_path = os.path.join(config_folder, file_name)

        #frame_positions_groupbox3 = []
        loaded_files = []

        for frame in self.frames_groupbox3:
            #x, y = frame.winfo_x(), frame.winfo_y()
            #frame_positions_groupbox3.append((x, y))
            loaded_files.append(frame)

        frame_positions_groupbox4 = []
        for frame in self.frames_groupbox4:
            x, y = frame.winfo_x(), frame.winfo_y()
            frame_positions_groupbox4.append((x, y))

        connections = []
        start_plugin = None
        for connection in self.canvas.connections:
            if 'start' in connection:
                start_plugin = connection['start']
            elif 'end' in connection and start_plugin:
                end_plugin = connection['end']
                line_id = connection.get('line_id', None)
                if line_id:
                    start_coords = self.canvas.coords(line_id)
                    if len(start_coords) >= 4:
                        start_x = start_coords[0]
                        start_y = start_coords[1]
                        end_x = start_coords[2]
                        end_y = start_coords[3]
                        connections.append({'start': start_plugin, 'end': end_plugin, 'start_x': start_x, 'start_y': start_y, 'end_x': end_x, 'end_y': end_y, 'line_id': line_id})
                start_plugin = None

        try:
            with open(file_path, 'w') as file:
                #file.write(f"frame_positions_groupbox3 = {frame_positions_groupbox3}\n")
                file.write(f"frame_positions_groupbox4 = {frame_positions_groupbox4}\n")
                file.write(f"connections = {connections}\n")
                file.write(f"loaded_files = {loaded_files}\n")
                file.write(f"\n")
                file.write(f"def load_saved_configuration(self):\n")
                file.write(f"    for frame, position in zip(self.frames_groupbox3, frame_positions_groupbox3):\n")
                file.write(f"        frame.place(x=position[0], y=position[1])\n")
                file.write(f"    for frame, position in zip(self.frames_groupbox4, frame_positions_groupbox4):\n")
                file.write(f"        frame.place(x=position[0], y=position[1])\n")
                file.write(f"    self.canvas.delete('line')\n")
                file.write(f"    for connection in connections:\n")
                file.write(f"        start_x = connection['start_x']\n")
                file.write(f"        start_y = connection['start_y']\n")
                file.write(f"        end_x = connection['end_x']\n")
                file.write(f"        end_y = connection['end_y']\n")
                file.write(f"        self.canvas.create_line(start_x, start_y, end_x, end_y, fill='red', width=2)\n")
                file.write(f"        self.canvas.connections.append({{'start': connection['start'], 'end': connection['end']}})\n")
                file.write(f"    for file_name in loaded_files:\n")
                file.write(f"        self.comboBox.set(file_name)\n")
                file.write(f"        self.load_selected_file()\n")
            messagebox.showinfo("Success", "Configuration saved successfully.")
        except Exception as e:
            print(f"Error occurred while saving configuration: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            
    def load_configuration(self, file_path):
        try:
            with open(file_path, 'r') as file:
                config_code = file.read()
                config_locals = {}
                exec(config_code, {}, config_locals)

            frame_positions_groupbox3 = config_locals.get('frame_positions_groupbox3', [])
            frame_positions_groupbox4 = config_locals.get('frame_positions_groupbox4', [])
            connections = config_locals.get('connections', [])
            loaded_files = config_locals.get('loaded_files', [])

            self.clear_frames()
            self.clear_plugins()

            for file_name in loaded_files:
                self.comboBox.set(file_name)
                self.load_selected_file()

            for frame, position in zip(self.frames_groupbox3, frame_positions_groupbox3):
                frame.place(x=position[0], y=position[1])

            for frame, position in zip(self.frames_groupbox4, frame_positions_groupbox4):
                frame.place(x=position[0], y=position[1])

            self.canvas.connections.clear()
            for connection in connections:
                start = connection['start']
                end = connection['end']
                start_coords = connection['start_coords']
                end_coords = connection['end_coords']
                line_id = self.canvas.create_line(start_coords[0], start_coords[1], end_coords[0], end_coords[1], fill="red", width=2)
                self.canvas.connections.append({'start': start, 'end': end, 'line_id': line_id})

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def save_configuration_dialog(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".py",
            filetypes=[("Python Files", "*.py")]
        )
        if file_path:
            self.save_configuration(file_path)
        else:
            messagebox.showwarning("Warning", "No file selected for saving the configuration.")
            
        # Update the dropdown menu with the new configuration file
        self.populate_saved_configurations()

    def load_configuration(self):
        print('\nloading configuration\n')
        selected_config = self.comboBox_2.get()
        if selected_config:
            config_folder = os.path.join(os.getcwd(), "config_new")
            file_path = os.path.join(config_folder, selected_config)
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"Configuration file not found: {selected_config}")
                return

            self.clear_frames()
            self.clear_plugins()

            try:
                with open(file_path, 'r') as file:
                    config_code = file.read()
                    config_locals = {}
                    exec(config_code, {}, config_locals)

                self.load_saved_configuration(config_locals)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")
        else:
            messagebox.showwarning("Warning", "No configuration file selected.")

    def load_saved_configuration(self, config_locals):
        self.clear_frames()
        self.clear_plugins()

        loaded_files = config_locals.get('loaded_files', [])
        frame_positions_groupbox3 = config_locals.get('frame_positions_groupbox3', [])
        frame_positions_groupbox4 = config_locals.get('frame_positions_groupbox4', [])
        connections = config_locals.get('connections', [])

        for file_name in loaded_files:
            self.comboBox.set(file_name)
            self.load_selected_file()


        for frame, position in zip(self.frames_groupbox4, frame_positions_groupbox4):
            x, y = position
            frame.place(x=x, y=y)

        self.canvas.connections.clear()  # Clear existing connections
        start.clear()  # Clear the start list
        end.clear()  # Clear the end list
        for connection in connections:
            start_plugin = connection['start']
            end_plugin = connection['end']
            start_x = connection['start_x']
            start_y = connection['start_y']
            end_x = connection['end_x']
            end_y = connection['end_y']
            line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, fill='red', width=2)
            self.canvas.connections.append({'start': start_plugin, 'end': end_plugin, 'line_id': line_id})
            start.append(start_plugin)  # Populate the start list
            if end_plugin not in end:  # Check if end_plugin is already in the end list
                end.append(end_plugin)  # Populate the end listt

        # Establish connections and transfer data between loaded plugins
        for connection in connections:
            start_plugin = None
            end_plugin = None
            for plugin_name, plugin_instance in opened_files_instances.items():
                if plugin_name == connection['start']:
                    start_plugin = plugin_instance
                if plugin_name == connection['end']:
                    end_plugin = plugin_instance
            if start_plugin and end_plugin:
                data = start_plugin.get_data()
                end_plugin.set_data(data)
                end_plugin.parent.update()  # Update the parent window to refresh the UI

    def populate_saved_configurations(self):
        config_folder = os.path.join(os.getcwd(), "config_new")
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        config_files = [file for file in os.listdir(config_folder) if file.endswith("_config.py")]
        result_list = sorted(config_files)
        self.comboBox_2["values"] = result_list

    def exit_application(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    ui = Ui_MainWindow(root)
    root.mainloop()