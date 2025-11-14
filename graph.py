import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from tkinter import messagebox
import tkinter as tk

class Grapher:
    def __init__(self):
        style.use('classic')
    
    def plot(self, file):
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(1, 1, 1)
        title = file.split('_')[0]  # Extract title from filename prefix
        
        # refresh the graph to show the data change live
        def animate(i):  # Changed parameter from 'file' to 'i'
            try:
                graphData = open(file, 'r').read()  # Use the file from outer scope
            except FileNotFoundError:
                # Create hidden root window for messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Hiba", "Nem létezik adatfájl!")
                root.destroy()
                return
            
            lines = graphData.split('\n')
            xs = []
            ys = []
            for line in lines:
                if len(line) > 1:
                    x, y = line.split(',')
                    try:
                        asd = y.split('~')
                        xs.append(float(x))
                        ys.append(float(asd[0]))
                    except:
                        xs.append(float(x))
                        ys.append(float(y))

            ax1.clear()
            ax1.plot(xs, ys)
            ax1.set_title(title)
            ax1.set_xlabel("Time (seconds)")
            try:
                ax1.set_ylabel(f"{title} ({asd[1]})")
            except:
                ax1.set_ylabel(title)
            

        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()

if __name__ == "__main__":
    Grapher().plot(sys.argv[1])