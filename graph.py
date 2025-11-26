import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

class Grapher:
    def __init__(self):
        style.use('bmh')
        self.paused = False
        self.live = True
        self.xs = []
        self.ys = []
        self.cursor_line = None
        self.cursor_point = None
        self.cursor_text = None
        self.last_cursor_x = None
        self.last_cursor_y = None
    
    def plot(self, file):
        """Plot live graph from the given data file."""
        file_path = file
        if file.startswith("./live_graphs/"):
            file = file[len("./live_graphs/"):]
        elif file.startswith("./graphs/"):
            self.live = False
            file = file[len("./graphs/"):]
        
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(1, 1, 1)
        title = file.split('_')[0]  # Extract title from filename prefix
        

        # Add pause functionality with spacebar
        def on_press(event):
            if event.key == ' ' and self.live:
                if self.paused:
                    ax1.set_title(title)
                    fig.canvas.draw()
                    print(f"{file} Resumed")
                    self.paused = False
                    ani.event_source.start()
                else:
                    ax1.set_title(title + " (Paused)")
                    fig.canvas.draw()
                    print(f"{file} Paused")
                    self.paused = True
                    ani.event_source.stop()

        def redraw_cursor(ax):
            """Redraw cursor elements after plot update"""
            if self.last_cursor_x is not None and self.last_cursor_y is not None and len(self.xs) > 0:
                # Find closest data point to last cursor position
                distances = np.abs(np.array(self.xs) - self.last_cursor_x)
                closest_idx = np.argmin(distances)
                
                if closest_idx < len(self.xs) and closest_idx < len(self.ys):
                    closest_x = self.xs[closest_idx]
                    closest_y = self.ys[closest_idx]
                    
                    # Add vertical line at cursor position
                    self.cursor_line = ax.axvline(x=closest_x, color='red', linestyle='--', alpha=0.7)
                    
                    # Add point at the data location
                    self.cursor_point = ax.plot(closest_x, closest_y, 'ro', markersize=6)[0]
                    
                    # Add text showing the values
                    y_range = max(self.ys) - min(self.ys) if len(self.ys) > 1 else 1
                    self.cursor_text = ax.text(closest_x, closest_y + y_range * 0.05, 
                                              f'({closest_x:.2f}, {closest_y:.2f})', 
                                              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                                              horizontalalignment='center')

        # Add mouse motion event for cursor
        def on_mouse_move(event):
            if event.inaxes != ax1 or len(self.xs) == 0:
                try:
                    self.last_cursor_x = None
                    self.last_cursor_y = None
                    self.cursor_line.remove()
                    self.cursor_line = None
                    self.cursor_point.remove()
                    self.cursor_point = None
                    self.cursor_text.remove()
                    self.cursor_text = None
                    return
                except:
                    return
            
            # Find the closest x value to cursor position
            if event.xdata is not None:
                # Store cursor position
                self.last_cursor_x = event.xdata
                
                # Find closest data point
                distances = np.abs(np.array(self.xs) - event.xdata)
                closest_idx = np.argmin(distances)
                
                if closest_idx < len(self.xs) and closest_idx < len(self.ys):
                    closest_x = self.xs[closest_idx]
                    closest_y = self.ys[closest_idx]
                    
                    # Store the actual data point position
                    self.last_cursor_y = closest_y
                    
                    # Remove previous cursor elements
                    if self.cursor_line:
                        self.cursor_line.remove()
                    if self.cursor_point:
                        self.cursor_point.remove()
                    if self.cursor_text:
                        self.cursor_text.remove()
                    
                    # Add vertical line at cursor position
                    self.cursor_line = ax1.axvline(x=closest_x, color='red', linestyle='--', alpha=0.7)
                    
                    # Add point at the data location
                    self.cursor_point = ax1.plot(closest_x, closest_y, 'ro', markersize=6)[0]
                    
                    # Add text showing the values
                    y_range = max(self.ys) - min(self.ys) if len(self.ys) > 1 else 1
                    self.cursor_text = ax1.text(closest_x, closest_y + y_range * 0.05, 
                                              f'({closest_x:.2f}, {closest_y:.2f})', 
                                              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                                              horizontalalignment='center')
                    
                    fig.canvas.draw_idle()
        
        # refresh the graph to show the data change live
        def animate(i):
            # Don't update if it's a saved graph (not live)
            if not self.live:
                return
                
            try:
                graphData = open(file_path, 'r').read()  # Use the file from outer scope
            except FileNotFoundError:
                # Create hidden root window for messagebox
                exit()
            
            lines = graphData.split('\n')
            self.xs = []
            self.ys = []
            for line in lines:
                if len(line) > 1:
                    x, y = line.split(',')
                    try:
                        asd = y.split('_')
                        self.xs.append(float(x))
                        self.ys.append(float(asd[0]))
                    except:
                        self.xs.append(float(x))
                        self.ys.append(float(y))

            ax1.clear()
            
            # Reset cursor elements references (they're cleared with ax1.clear())
            self.cursor_line = None
            self.cursor_point = None
            self.cursor_text = None
            
            ax1.plot(self.xs, self.ys)
            ax1.set_title(title)
            ax1.set_xlabel("Time (seconds)")
            try:
                ax1.set_ylabel(f"{title} ({asd[1]})")
            except:
                ax1.set_ylabel(title)
            
            # Redraw cursor if it was previously shown
            redraw_cursor(ax1)

        
        ani = animation.FuncAnimation(fig, animate, interval=100)

        # For saved graphs, load the data once and display it
        if not self.live:
            # Load and display the saved graph data once
            try:
                graphData = open(file_path, 'r').read()
                lines = graphData.split('\n')
                self.xs = []
                self.ys = []
                for line in lines:
                    if len(line) > 1:
                        x, y = line.split(',')
                        try:
                            asd = y.split('_')
                            self.xs.append(float(x))
                            self.ys.append(float(asd[0]))
                        except:
                            self.xs.append(float(x))
                            self.ys.append(float(y))

                ax1.plot(self.xs, self.ys)
                ax1.set_title(title + f" (From {file.split('_')[1][0:4]}.{file.split('_')[1][4:6]}.{file.split('_')[1][6:8]}. {file.split('_')[2][0:2]}:{file.split('_')[2][2:4]}:{file.split('_')[2][4:6]})")
                ax1.set_xlabel("Time (seconds)")
                try:
                    ax1.set_ylabel(f"{title} ({asd[1]})")
                except:
                    ax1.set_ylabel(title)
                    
            except FileNotFoundError:
                ax1.set_title("File not found")
        
        # Start paused if it's a saved graph
        if not self.live:
            ani.event_source.stop()

        
        # Connect the events
        fig.canvas.mpl_connect('key_press_event', on_press)
        fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

        plt.show()

if __name__ == "__main__":
    Grapher().plot(sys.argv[1])