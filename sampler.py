import time
import random

graph_file = open("graph_data.txt", "w")

# sample_rate = float(input("Adja meg a mintavételi rátát másodpercben: "))
# sample_type = input("Adja meg a mintavétel típusát:\n - random\n - szinusz")

sample_rate = 1.0
sample_type = "random"

x = 0

if sample_type == "random":
    while True:
        x = x + 1
        y = random.randint(0, 300)
        print(f"{x},{y}")
        graph_file.write(f"{x},{y}\n")
        graph_file.flush()
        time.sleep(sample_rate)

elif sample_type == "szinusz":
    while True:
        import math
        x = x + 1
        y = 150 + 100 * math.sin(x * 0.2)
        print(f"{x},{y}")
        graph_file.write(f"{x},{y}\n")
        graph_file.flush()
        time.sleep(sample_rate)