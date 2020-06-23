# Parampreet Singh - 22/06/20
# Matplotlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
# Basic Graph
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Resize
plt.figure(figsize=(5, 3), dpi=100)  # dpi = pixel per inch

# fmt = "[colour][marker][line]"
plt.plot(x, y, "rx--", la bel="x")  # Short hand notation
#plt.plot(x, y, "rx-- ", label="Line", c="red", marker="x", linestyle="--")

# Second line
x2 = np.arange(0, 4, 0.5)
plt.plot(x2, x2**2, label="x2**2")

plt.title("Graph 1", fontdict={"fontname": "Comic Sans MS", "fontsize": 20})

plt.xlabel("X axis")
plt.ylabel("Y axis")

plt.xticks(x)
plt.yticks(y)

plt.legend()
plt.savefig("mygraph.png", dpi=300)
plt.show()

# Bar chart
labels = ["A", "B", "C"]
values = [1, 4, 2]

bars = plt.bar(labels, values)

bars[0].set_hatch("/")
bars[1].set_hatch("o")
bars[2].set_hatch("*")
plt.show()


# Real world examples
gas = pd.read_csv("gas_prices.csv")
plt.figure(0)
plt.plot(gas.Year, gas.USA, "rx-", label="USA")
plt.plot(gas.Year, gas.Canada, "b.-", label="Canada")

plt.title("USA vs Canada Gas Prices")
plt.xlabel("Year")
plt.ylabel("Dollar/Gallon")
plt.legend()

plt.xticks(gas.Year[::3].tolist()+[2011])

plt.show()

# Histogram
bins = [40, 50, 60, 70, 80, 90, 100]
fifa = pd.read_csv("fifa_data.csv")
print(fifa.head(5))

plt.hist(fifa.Overall, bins=bins)
plt.xticks(bins)
plt.ylabel("Number of players")
plt.xlabel("Skill Level")
plt.title("Distribution of player skills in FIFA 2018")

plt.show()

# Pie Chart
fifa = pd.read_csv("fifa_data.csv")
left = fifa.loc[fifa["Preferred Foot"] == "Left"].count()[0]
right = fifa.loc[fifa["Preferred Foot"] == "Right"].count()[0]

labels = ["Left", "Right"]
plt.pie([left, right], labels=labels, autopct="%.2f %%")
plt.title("Foot Preference of Fifa players")

plt.show()
"""
