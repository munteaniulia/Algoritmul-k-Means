import math
import random
from copy import deepcopy
from random import randint
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.animation import FuncAnimation

sys.setrecursionlimit(10000000)

file_name = 'coord_X_coord_Y_index_Zona.txt'
centroizi_file_name = "Centroizi.txt"

# Define zones
nrOfCentroizi = randint(2, 10)
zona1 = {"name": "zona1", "mx": 180, "my": 220, "sigmax": 10, "sigmay": 10}
zona2 = {"name": "zona2", "mx": -100, "my": 110, "sigmax": 15, "sigmay": 10}
zona3 = {"name": "zona3", "mx": 210, "my": -150, "sigmax": 5, "sigmay": 20}
culori_zona = {'zona1': 'red', 'zona2': 'blue', 'zona3': 'green'}

# Initialize variables
X, Y, culori_initiale = [], [], []
centroizi, cluster_dict, cluster_colors = [], {}, []
E_trecut = None

# Helper functions
def alege_valoarea_pt_coord():
    return randint(-300, 300)

def convertire(coord, zona, xORy):
    return np.exp(-((zona[f"m{xORy}"] - coord) ** 2) / (2 * (zona[f"sigma{xORy}"] ** 2)))

def verificare_nr_puncte():
    with open(file_name, 'r') as f:
        if len(f.readlines()) < 10000:
            zona = random.choice([zona1, zona2, zona3])
            x = alege_valoarea_pt_coord()
            verifPragx(x, zona)

def verifPragy(y, zona):
    yConvert = convertire(y, zona, "y")
    prag = round(random.random(), 3)
    if yConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{y} {zona['name']}\n")
        verificare_nr_puncte()
    else:
        verifPragy(alege_valoarea_pt_coord(), zona)

def verifPragx(x, zona):
    xConvert = convertire(x, zona, "x")
    prag = round(random.random(), 3)
    if xConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{x} ")
        verifPragy(alege_valoarea_pt_coord(), zona)
    else:
        verifPragx(alege_valoarea_pt_coord(), zona)

def generareCentroizi():
    k = nrOfCentroizi
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'deeppink', 'greenyellow']
    while k > 0:
        with open(centroizi_file_name, 'a') as f:
            x, y = randint(-300, 300), randint(-300, 300)
            centroizi.append((x, y))
            cluster_dict[(x, y)] = []
            f.write(f"{x} {y}\n")
        cluster_colors.append(colors[k-1])
        k -= 1


def distanta_Euclidiana(centroid, punct):
    return math.sqrt((centroid[0] - punct[0]) ** 2 + (centroid[1] - punct[1]) ** 2)

def grupareDupaCentroid():
    puncte_clusters = []
    with open(file_name, 'r') as f:
        for punct in f:
            punct = punct.split()
            distanta_minima, centroid_apropiat = float('inf'), None
            punct = (int(punct[0]), int(punct[1]))
            min_index = 0
            for i, centroid in enumerate(centroizi):
                distanta = distanta_Euclidiana(centroid, punct)
                if distanta < distanta_minima:
                    distanta_minima, centroid_apropiat, min_index = distanta, centroid, i
            cluster_dict[centroid_apropiat].append(punct)
            puncte_clusters.append(min_index)
    return puncte_clusters

def calculCentruDeGreutate():
    temp = deepcopy(cluster_dict)
    centroizi.clear()
    for centroid, puncte in temp.items():
        if puncte:
            media_x = float(np.mean([punct[0] for punct in puncte]))
            media_y = float(np.mean([punct[1] for punct in puncte]))
            cluster_dict[(media_x, media_y)] = cluster_dict.pop(centroid)
            centroizi.append((media_x, media_y))
        else:
            centroizi.append(centroid)

def convergenta():
    return sum(distanta_Euclidiana(centroid, punct) for centroid, puncte in cluster_dict.items() for punct in puncte)

def stergerePuncte():
    for centroid in cluster_dict:
        cluster_dict[centroid] = []

Zona = random.choice([zona1, zona2, zona3])
verifPragx(alege_valoarea_pt_coord(), Zona)

# Load dataset
with open(file_name, 'r') as f:
    for linie in f:
        coordonate = linie.split()
        X.append(float(coordonate[0]))
        Y.append(float(coordonate[1]))
        culori_initiale.append('pink')  # Initial color for points

# Initialize k-means
generareCentroizi()

# Create figure for animation
fig, ax = plt.subplots()
scat = ax.scatter(X, Y, c=culori_initiale, s=0.5)
centroids_plot, = ax.plot([], [], 'ko', markersize=4)

ax.axhline(0, color='black', linewidth=0.9)
ax.axvline(0, color='black', linewidth=0.9)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("k-Means Clustering Animation")

def update(frame):
    global E_trecut, E_curent
    stergerePuncte()
    puncte_clusters = grupareDupaCentroid()
    calculCentruDeGreutate()
    E_curent = round(convergenta(), 4)

    # Stop the animation when converged
    if E_trecut == E_curent:
        ani.event_source.stop()
    E_trecut = E_curent

    # Update points colors based on cluster assignments
    culori_actualizate = [cluster_colors[cluster] for cluster in puncte_clusters]
    scat.set_color(culori_actualizate)

    # Update centroid positions
    cx, cy = zip(*centroizi)
    centroids_plot.set_data(cx, cy)
    return scat, centroids_plot

ani = FuncAnimation(fig, update, frames=np.arange(0, 100), repeat=False)
plt.show()