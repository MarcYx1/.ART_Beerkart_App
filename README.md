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

![screenshot of the app](https://media.discordapp.net/attachments/906544961523171398/1443047330151399474/image.png?ex=6927a60e&is=6926548e&hm=8ae163c39aca30df1b077a20eb54a40448484b4506f23d05dc792867a6291310&=&format=webp&quality=lossless)

## Reading data over serial
To start sampling data from the Beerkart we need to choose the serial port on which the Beerkart is connected.

![screenshot of the serial connection frame](https://cdn.discordapp.com/attachments/906544961523171398/1443049653363937452/image.png?ex=6927a837&is=692656b7&hm=9c8f39c09fb869d442510cc3df879781060736966a1cb1c02bb708989666961b&)

After the serial connection doesen't show an error and the status label states "Connected", we must start the sampler script. This is the heart of the sampling process.

![Screenshot of the data graph frame with the sampler buttons and label boxed with red](https://media.discordapp.net/attachments/906544961523171398/1443051095168389271/image.png?ex=6927a98f&is=6926580f&hm=7357b3123f58104a0b5a032c560a44693697a4a3e2188a7a521c77b989606517&=&format=webp&quality=lossless)

If it's still going without errors and the status label states "Running" the sampler is succesfully connected and as soon as it recieves data from its serial connection, files should pop up in `./live_graphs` in the following format: `(data_name)_(date)_(time).txt` eg.: `voltage_20251126_023411.txt`

Now we can view these datas plotted onto a graph by clicking the Live Graph(s) button.

![screenshot of graphs frame](https://media.discordapp.net/attachments/906544961523171398/1443052617642016940/image.png?ex=6927aafa&is=6926597a&hm=9fdda1208e2f24b6304c4fde48d09e2526348342903eff0e05192f37c2e78d42&=&format=webp&quality=lossless)

A file selection window will appear, select the data files you wish viewing.

![screenshot of file selection window](https://media.discordapp.net/attachments/906544961523171398/1443053215959486625/image.png?ex=6927ab89&is=69265a09&hm=a886809ec521927a85af3dc7570d35976867ff4cdfc8d6c250618558e67a1354&=&format=webp&quality=lossless)

This will open the selected graph files in seperate [matpotlib](https://github.com/matplotlib/matplotlib) windows.

![screenshot of graphs](https://cdn.discordapp.com/attachments/906544961523171398/1443054077595353128/image.png?ex=6927ac56&is=69265ad6&hm=c350eacaab1e596218f6b9ef7a8f0437123af1082c5be9a42f2d64798f6148bd&)

Howering over the graph will show cursor readout that displays a line of which data its currently displaying and the data of the two axis eg.: (time,data) or (13.40,105.32).

![screenshot of a graph with the redout feature showing](https://media.discordapp.net/attachments/906544961523171398/1443055961571983410/image.png?ex=6927ae17&is=69265c97&hm=b6ddab80db62563f249572a64b67b398bf74711f88736a82e985cf2cac74b65e&=&format=webp&quality=lossless)


A live graph can be paused by pressing SPACE when the grap window is focused. In this state the magnify glass button allows the user to zoom, the axis button allows the user to move around the graph for better viewing.

![screenshot of a graph with buttons highlighted](https://media.discordapp.net/attachments/906544961523171398/1443055256563880060/image.png?ex=6927ad6f&is=69265bef&hm=9662ee09327ff04f8ca5e9b5530a481cb8e3ebf67e8054b8ad1d4bb05d3a2c53&=&format=webp&quality=lossless)

After stopping the sampler the files from `./live_graphs` are moved to `./graphs`. Opening these data files are just as simple as opening live data files, pressing the Saved Graph(s) button will show a file selection window with the saved graph(s).
Deleting saved graph(s) is also possible with the Delete Graph Files button which will also show a file selection window.

## Sending power limit/sampling rate over serial
It is very straightforward, set the slider or enter a number into the entry and press send. This goes for sampling rate aswell.

![screenshot of the power limit slider and entry](https://media.discordapp.net/attachments/906544961523171398/1443057570670706832/image.png?ex=6927af97&is=69265e17&hm=4744d54eb7dbfd6b0a5f35b6b7180afb0fe9927ef2750f2542991abd06388a4a&=&format=webp&quality=lossless)

## Changing the theme
Changing the theme is possible by pressing the sun/moon icon on the bottom left above the version indication label. This sets the theme of every sub window except graphs, graphs always use a light color theme. Theme of the window automatically matches system's theme.

### Light theme windows
Main window:

![Screenshot of light theme main window](https://media.discordapp.net/attachments/906544961523171398/1443058390585708676/image.png?ex=6927b05b&is=69265edb&hm=c9c22d449c75d7a486a672be7723393b3fb6ba32d9c218657146fd7e7060d2df&=&format=webp&quality=lossless)

File selection window:

![screenshot of file selection window in light theme](https://media.discordapp.net/attachments/906544961523171398/1443058703493234849/image.png?ex=6927b0a5&is=69265f25&hm=20411ea2b493c31db6716a776ed1348b46549138f96852505cc4dd58715f622b&=&format=webp&quality=lossless)

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

# KNOWN BUGS:
- ~~Sampler is not stopped by the sample stop button~~
- ~~Sometimes the data line gets out of phase...~~  
- ~~Disconnect button does not stop sampler either~~
- Sampler needs to be connected to send power data, should be unrelated to sampler running.
- ~~Light mode is buggy, I should’ve used styling instead of hardcoding colors~~
