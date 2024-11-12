import math
import random
from copy import deepcopy
from random import randint
import matplotlib.pyplot as plt
import sys
import numpy as np
import time  # Importăm modulul pentru pauze

sys.setrecursionlimit(10000000)

file_name = 'coord_X_coord_Y_index_Zona.txt'
centroizi_file_name = "Centroizi.txt"

# Definirea zonelor și culorilor
nrOfCentroizi = randint(2, 10)
zona1 = {"name": "zona1", "mx": 180, "my": 220, "sigmax": 10, "sigmay": 10}
zona2 = {"name": "zona2", "mx": -100, "my": 110, "sigmax": 15, "sigmay": 10}
zona3 = {"name": "zona3", "mx": 210, "my": -150, "sigmax": 5, "sigmay": 20}
culori_zona = {'zona1': 'red', 'zona2': 'blue', 'zona3': 'green'}

X, Y, culori, centroizi, cluster_dict = [], [], [], [], {}
E_trecut = None


def alege_valoarea_pt_coord():
    return randint(-300, 300)


def convertire(coord, zona, xORy):
    return np.exp(-((zona[f"m{xORy}"] - coord) ** 2) / (2 * (zona[f"sigma{xORy}"] ** 2)))


def verificare_nr_puncte():
    with open(file_name, 'r') as f:
        numar_linii = len(f.readlines())
    if numar_linii < 10000:
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
        y = alege_valoarea_pt_coord()
        verifPragy(y, zona)


def verifPragx(x, zona):
    xConvert = convertire(x, zona, "x")
    prag = round(random.random(), 3)
    if xConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{x} ")
        coordy = alege_valoarea_pt_coord()
        verifPragy(coordy, zona)
    else:
        x = alege_valoarea_pt_coord()
        verifPragx(x, zona)


def generareCentroizi():
    k = nrOfCentroizi
    while k > 0:
        with open(centroizi_file_name, 'a') as f:
            x, y = randint(-300, 300), randint(-300, 300)
            centroizi.append((x, y))
            cluster_dict[(x, y)] = []
            f.write(f"{x} {y}\n")
        k -= 1


def distanta_Euclidiana(centroid, punct):
    return math.sqrt((centroid[0] - punct[0]) ** 2 + (centroid[1] - punct[1]) ** 2)


def grupareDupaCentroid():
    with open(file_name, 'r') as f:
        for linie in f:
            coordonate = linie.split()
            punct = (int(coordonate[0]), int(coordonate[1]))
            distanta_minima, centroid_apropiat = float('inf'), None
            for centroid in centroizi:
                distanta = distanta_Euclidiana(centroid, punct)
                if distanta < distanta_minima:
                    distanta_minima, centroid_apropiat = distanta, centroid
            cluster_dict[centroid_apropiat].append(punct)


def calculCentruDeGreutate():
    temp = deepcopy(cluster_dict)
    centroizi.clear()
    for centroid, puncte in temp.items():
        if puncte:
            media_x, media_y = np.mean([p[0] for p in puncte]), np.mean([p[1] for p in puncte])
            cluster_dict[(media_x, media_y)] = cluster_dict.pop(centroid)
            centroizi.append((media_x, media_y))
        else:
            centroizi.append(centroid)


def convergenta():
    E_curent = sum(
        distanta_Euclidiana(centroid, punct) for centroid, puncte in cluster_dict.items() for punct in puncte)
    return E_curent


def stergerePuncte():
    for centroid in cluster_dict:
        cluster_dict[centroid] = []


# Generare puncte
Zona = random.choice([zona1, zona2, zona3])
x = alege_valoarea_pt_coord()
verifPragx(x, Zona)

# Citire puncte și zone pentru colorare
with open(file_name, 'r') as f:
    for linie in f:
        coordonate = linie.split()
        X.append(float(coordonate[0]))
        Y.append(float(coordonate[1]))
        zona = coordonate[2]
        culori.append(culori_zona[zona])

plt.figure()
plt.scatter(X, Y, c=culori, s=0.5)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Punctele colorate în funcție de zona")
plt.axhline(0, color='black', linewidth=0.9)
plt.axvline(0, color='black', linewidth=0.9)

# K-Means clustering și afișare pe epoci
generareCentroizi()
grupareDupaCentroid()
calculCentruDeGreutate()
E_curent = round(convergenta(), 4)
epoca = 0

while True:
    plt.figure()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(centroizi)))
    for idx, (centroid, puncte) in enumerate(cluster_dict.items()):
        cx, cy = zip(*puncte) if puncte else ([], [])
        plt.scatter(cx, cy, color=colors[idx], s=1)
    plt.scatter(*zip(*centroizi), color='black', s=10, marker='x')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Epoca {epoca}")
    plt.pause(0.5)

    if E_trecut == E_curent:
        break
    E_trecut = E_curent
    stergerePuncte()
    grupareDupaCentroid()
    calculCentruDeGreutate()
    E_curent = round(convergenta(), 4)
    epoca += 1

plt.show()
