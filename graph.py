import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('classic')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# refresh the graph to show the data change live
def animate(i):
    try:
        graphData = open('graph_data.txt', 'r').read()
    except FileNotFoundError:
        print("Nem létezik adatfájl!")
        return
    
    lines = graphData.split('\n')
    xs = []
    ys = []

    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))

    ax1.clear()
    ax1.plot(xs, ys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()