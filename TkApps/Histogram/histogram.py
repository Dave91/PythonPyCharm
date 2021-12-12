import matplotlib.pyplot as plt
import pandas as pd

'''tenyget = self.optmenu.get()
tenyezo = {"Ötöslottó": "otos", "Hatoslottó": "hatos"}
pdread = pd.read_csv("data/" + tenyezo[tenyget] + ".csv", delimiter=";")'''

pdread = pd.read_csv("data/otos.csv", delimiter=";")

kern = []
for i in range(1, 6):
    yval = pdread["#" + str(i)]
    for yl in iter(yval):
        kern.append(yl)
# print(kern)
huzottn = []
for k in range(1, 91):
    nm = 0
    for kn in kern:
        if kn == k:
            nm += 1
    huzottn.append(nm)
# print(huzottn)

xn = range(1, 91)
fig = plt.figure(figsize=(12, 4))
canv = plt.FigureCanvasBase(fig)
canv.draw()
plt.bar(xn, height=huzottn, color="lightblue", edgecolor="grey")
plt.xticks(xn, xn, rotation=90, fontsize=6)
plt.yticks(fontsize=6)
plt.xlabel("Lottószámok (1-90)", fontsize=8)
plt.ylabel("Érték ", fontsize=8)
plt.title("Kihúzott lottószámok megoszlása (Ötös)", fontsize=8)
# plt.ylim(min(huzottn) - min(huzottn) * 0.2, max(huzottn) + max(huzottn) * 0.2)
plt.grid(which="major", axis="y")
# fig.tight_layout()
plt.show()
