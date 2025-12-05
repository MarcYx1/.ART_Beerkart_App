# ART Beerkart Manager App
A python based GUI app for the beerkart.

The app allows us to recieve data over serial from the beerkart's CANBUS for logging and set the power limit for the electric motor without intrusive changes.

Features:
- Sampling data from serial
- Graphing sampled data
- Save sampled data
- Send power limit and sampling rate over serial
- Light theme

# The app
### Main Window
The app uses [custom tkinter](https://github.com/TomSchimansky/CustomTkinter) to display a modern main window acting as a hub to all the feature it contains.

<img alt="screenshot of the app" width="773" height="594" alt="image" src="https://github.com/user-attachments/assets/bb34d21b-419c-4e7f-b7ba-d1c712e3416b" />


## Reading data over serial
To start sampling data from the Beerkart we need to choose the serial port on which the Beerkart is connected.

<img width="366" height="208" alt="image" src="https://github.com/user-attachments/assets/e4c3aa44-1708-47e3-bc06-4d1bae88b67f" />


After the serial connection doesen't show an error and the status label states "Connected", we must start the sampler script. This is the heart of the sampling process.

<img width="391" height="337" alt="image" src="https://github.com/user-attachments/assets/3133f7b9-53a5-42a8-b533-0f93a8a15779" />


If it's still going without errors and the status label states "Running" the sampler is succesfully connected and as soon as it recieves data from its serial connection, files should pop up in `./live_graphs` in the following format: `(data_name)_(date)_(time).txt` eg.: `voltage_20251126_023411.txt`

Now we can view these datas plotted onto a graph by clicking the Live Graph(s) button.

<img width="388" height="147" alt="image" src="https://github.com/user-attachments/assets/2d9eddb0-c3f1-4f26-a4f2-1f3c61af1348" />


A file selection window will appear, select the data files you wish viewing.

<img width="396" height="326" alt="image" src="https://github.com/user-attachments/assets/718b4f63-c532-4ffc-838d-c69f830734bb" />


This will open the selected graph files in seperate [matpotlib](https://github.com/matplotlib/matplotlib) windows.

<img width="1279" height="981" alt="image" src="https://github.com/user-attachments/assets/c2fd116d-e8a2-4cbf-9acd-a1c689d1f267" />


Howering over the graph will show cursor readout that displays a line of which data its currently displaying and the data of the two axis eg.: (time,data) or (13.40,105.32).

<img width="997" height="667" alt="image" src="https://github.com/user-attachments/assets/068207cc-6ebd-4aa4-86f6-85e9af8c0d1d" />


A live graph can be paused by pressing SPACE when the grap window is focused. In this state the magnify glass button allows the user to zoom, the axis button allows the user to move around the graph for better viewing.

<img width="998" height="669" alt="image" src="https://github.com/user-attachments/assets/e4d76c58-d2e3-4fc5-a2a2-e6877a37da71" />

After stopping the sampler the files from `./live_graphs` are moved to `./graphs`. Opening these data files are just as simple as opening live data files, pressing the Saved Graph(s) button will show a file selection window with the saved graph(s).
Deleting saved graph(s) is also possible with the Delete Graph Files button which will also show a file selection window.

## Sending power limit/sampling rate over serial
It is very straightforward, set the slider or enter a number into the entry and press send. This goes for sampling rate aswell.

<img width="360" height="139" alt="image" src="https://github.com/user-attachments/assets/9c296660-bec8-4cb7-9200-64767e1d39e0" />

## Changing the theme
Changing the theme is possible by pressing the sun/moon icon on the bottom left above the version indication label. This sets the theme of every sub window except graphs, graphs always use a light color theme. Theme of the window automatically matches system's theme.

### Light theme windows
Main window:

<img width="766" height="589" alt="image" src="https://github.com/user-attachments/assets/791b6eb0-6e56-4ea8-9e4d-5998c0c59011" />

File selection window:

<img width="399" height="325" alt="image" src="https://github.com/user-attachments/assets/14b4e32a-e3a7-4138-9fe8-2fcaff5cf1df" />

# Installation (untill release):
Requires:
- Python 3.11.5+
- [pip](https://pip.pypa.io/en/stable/installation/#get-pip-py) for installing packages

1. [Download the source code](https://github.com/MarcYx1/.ART_Beerkart_App/archive/refs/heads/main.zip)
2. run `pip install -r dependencies.txt` in CMD inside the source code's directory
3. run Main.py

An .exe build will be avaliable on release.





# TODO:
- ~~**TOP PRIORITY !!! CANbus connection and communication**~~ (We're keeping serial, changing to CAN would take too much work for not a lot of pros)
- ✓ ~~Serial connection~~
- ✓ ~~Option to save sampled data (v0.3 technically makes this a thing, the data is being saved into a file)~~
- ✓ ~~IDK yet but if we need to sample multiple data at once, multiple graphs at once, maybe when pressing live graph the user should be able to choose the graph he wants to open?~~
- ✓ ~~The entire sampler script, which includes serial connection (TOP PRIORITY)~~
- Heartbeat indicator
- ✓ ~~Script only reads data rn, sending is not yet implemented~~
- ✓ ~~Maybe a check graph button next to live graph(s) which allows user to choose previous graphs to show~~
- ✓ ~~Pause sampler button~~
- .xlsx export
- ✓ ~~**Open Graph(s)** button may ask user which graph files to open and indicate which are live~~
- ✓ ~~**Delete Graph Files** button may ask user which graph files to delete, disallow deletion of live files~~
- ✓ ~~Light theme~~
- ✓ ~~Maybe rework the saved graph choice menu, instead of just picking a file make a dedicated window that shows a clean list of files. (eg.: name | date | time)~~
- Warning indicators in monitoring window for exceeding temp or voltage limits of a cell

# KNOWN BUGS:
- ~~Sampler is not stopped by the sample stop button~~
- ~~Sometimes the data line gets out of phase...~~  
- ~~Disconnect button does not stop sampler either~~
- Sampler needs to be connected to send power data, should be unrelated to sampler running.
- ~~Light mode is buggy, I should’ve used styling instead of hardcoding colors~~
- I did not realize handlind this much .txt files will be very inefficient. May have to rework the entire data system to work with one .json / cell instead of data type. (will see if the performance issue is noticable whe using it live)