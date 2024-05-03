Here you will find 4 folder in total:
1. SI-2 Mac (executable Mac file)
2. SI-2 Windows (executable Windows file)
3. SI-2 Code
4. Individual Frames TXT

Prerequisites:
- Python 3.10.6
- Python libraries numpy,matplotlib,PIL,pillow

To run SI2 using executable files:
- open the SI-2 Mac or SI-2 Windows
- Navigate to dist folder and run SI2 to start application.
- In the dropdown menu corresponding to new buttons you will see the plugins as pyc files
- Select those pyc files in order thermalFile.pyc, thermalVisualizer.pyc, display.pyc
- Now in PluginGroupBox you will see their plugin graphs.
- left click on Thermal(red button) and right click on Thermal(green button), left click on Image(red button) and right click on Image(green button) to create the connections.
- You can see lines that are visible to us to verify they are connected.
- Now if you open the User Interface tab you can see the plugins corresponding UI which is loaded into the UIGroupBox.
- You can reposition them by clicking on the borders of the UI and dragging them across the UIGroupBox.
- In thermalFile UI, you can click on open button and select individual frame text file which is in IndividualFramesTXT folder to load it into thermalFile.
- You can verify the selected file in the UI of thermalFile.
- Now click on the start button which is on the bottom left to start the data flow from one plugin to another plugin.
- When you change the min max temperature in thermalVisualizer you can see that the image in display plugin is changed accordingly.
- To pause the dataflow, you can click on pause button when the data is transferring.
- Navigate back to plugin graph and click on save button which gives you option to select the folder to save the configuration. Open the project folder and save the configuration in “dist/config_new/” and give the appropriate name to the configuration and click on save.
- To load the saved configuration, click on dropdown menu corresponding to the load/save configuration and click on load button to load the saved configuration.
- This will also save the positions of the User Interface in the User Interface tab.
- To clear the plugins, you need to click on New button which will clear all the plugins and connections and their corresponding UI.
- To close the application safely, you can click on exit button which is on the bottom right corner of the application. 

To run SI2 using code files:
- Navigate to the SI2 code folder from the terminal and run the command "python3 SI2.py" to start the application.
- From here it's just same steps mentioned above to work with the application.


Lets know about Code:
- Here we have SI2.py file which is our main file handles all the User Interface implementation of SI2.
- thermalFile.py is a file which opens the thermal txt files one after the other and it returns the array which is in the txt file.
- thermalVisualizer.py is a file which takes array as input and apply color mapping to the array and convert it to image and returns the image.
- display.py is a file which takes image as input and display it in the frame and it returns None.
- setup_for_pyc.py is a file which generates .pyc file from .py file. You need to use command "python3 setup_for_pyc.py thermalFile.py" in your terminal which generates pyc file for thermalFile.py in the same folder. Similarly for display.py you can generate .pyc using "python3 setup_for_pyc.py display.py".
- setup_for_exe.py is a python file to generate executable folder Mac or for Windows. You just need to execute the file to generate exe files. Before that you need to install pyinstaller package using "pip install pyinstaller" in the terminal.

Switch Usage between pyc and py:
- If you want to use py files instead of pyc file to load into SI2 you can navigate to populate_pyc_files which is inside UI_MainWindow class and replace "pyc_files = [file for file in os.listdir(current_directory) if file.endswith(".pyc")] " line with " pyc_files = [file for file in os.listdir(current_directory) if file.endswith(".py")] ".
- Now if you run SI2 file from terminal in dropdown menu corresponding to new button you could access python files and load them same as a pyc file.