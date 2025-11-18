# ART Beerkart Manager App

### TODO:
    - ✓ Serial connection
    - ✓ Option to save sampled data (v0.3 technically makes this a thing, the data is being saved into a file)
    - ✓ IDK yet but if we need to sample multiple data at once, multiple graphs at once, maybe when pressing live graph the user should be able to choose the graph he wants to open?
    - ✓ The entire sampler script, which includes serial connection (TOP PRIORITY)
    - Heartbeat indicator
    - ✓ Script only reads data rn, sending is not yet implemented
    - CANbus connection?!
    - Maybe a check graph button next to live graph(s) which allows user to choose previous graphs to show
    - ✓ Pause sampler button
    - .xlsx export
    - **Open Graph(s)** button may ask user which graph files to open and indicate which are live
    - **Delete Graph Files** button may ask user which graph files to delete, disallow deletion of live files

### BUGS:
    - Sampler is not stopped by the sample stop button
    - Sometimes the data line gets out of phase and the name of a file starts at the wrong character
    - Disconnect button does not stop sampler either
    - Not really a bug but: sampler needs to be connected to send power data, it should be unrelated to sampler running.