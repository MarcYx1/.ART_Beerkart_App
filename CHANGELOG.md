## first commit
- Made the foundation files for the project

## v0.1
- Some changes to the UI, still non functioning.

## v0.1.1
- Some changes to the UI, still non functioning.

## v0.2
- Serial now works with some bugs that needs fixing

## v0.3
- Bugfixes
- Multiple graphs now are working fully
- Added graph data delete button
- graph now shows data name, title and unit of measurement
- CHANGELOG.md lacked markdown indicators now does
- Data sampling basically works with some bugs

## v0.3.1
- Removed Herobrine

## v0.4
- Sampler stop button now actually stops the sampler
- Disconnect button also stops sampler
- Added missing send button from sampling rate (lol?)
- Powerlimit sending over serial is now implemented. Uses the same format it recieves data e.g.: f'power={percentage}'
- Rate sending over serial is now implemented. Uses the same format it recieves data e.g.: f'rate={ms}'
- UI beauty changes, removed the boxes around the two rows in the left coloumn

## V0.4.1
- Remove Herobrine

## V0.5
- Reworked graph button
    * Made seperate button for live and saved graph data files
    * Added file dialog for graph deletion
    * Added file dialog for choosing saved graph files
- WIP Light theme
- Moved pictures and icons into ./assets

## V0.6
- ACTUALLY fixed sampler not stopping (idk what I was thinking when trying to kill a thread instead of just calling disconnect() ¯\_(ツ)_/¯)
- Better graph handling
    * Saved and live graphs are now seperately saved to ./graphs and ./live_graphs
    * Graph delete now shows a file dialog instead of deleting every graph data file
    * Saved graphs also show a file dialog
- graph.py now handles subdirectories correctly
- Light theme implemented
- Markdown formatting lol, i forgor 💀

## V0.6.1
- WIP better file selection window with custom tkinter

## V0.7
- Reworked file selection for better readability
    * Opening live graph files, saved graph files and deleting graph files now open a dedicated window
    * Follows theme of main window
- Color theme now follows system
- Added version indication label to GUI