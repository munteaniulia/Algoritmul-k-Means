import math
import random
from array import array
from random import randint
import matplotlib.pyplot as plt
import sys
import numpy as np

sys.setrecursionlimit(10000000)

file_name = 'coord_X_coord_Y_index_Zona.txt'
centroizi_file_name= "Centroizi.txt"

nrOfCentroizi = randint(2, 10)
zona1={
    "name": "zona1",
    "mx": 180,
    "my": 220,
    "sigmax":10,
    "sigmay":10,
}
zona2={
    "name": "zona2",
    "mx": -100,
    "my": 110,
    "sigmax":15,
    "sigmay":10,
}
zona3={
    "name": "zona3",
    "mx": 210,
    "my": -150,
    "sigmax": 5,
    "sigmay": 20,
}
culori_zona = {
    'zona1': 'red',
    'zona2': 'blue',
    'zona3': 'green'
}
X = []
Y = []
culori = []
numarDeCentroizi = randint(2, 10)

def alege_valoarea_pt_coord():
    coord=randint(-300,300)
    return coord

def convertire(coord, zona, xORy):
    coordConvert = np.exp(-((zona[f"m{xORy}"] - coord) ** 2) / (2 * (zona[f"sigma{xORy}"] ** 2)))

    return coordConvert

def verificare_nr_puncte():
    with open(file_name , 'r') as f:
        linii = f.readlines()

    numar_linii = len(linii)
    if numar_linii < 10000:
        zona = random.choice([zona1, zona2, zona3])
        x = alege_valoarea_pt_coord()
        verifPragx(x,zona)

def verifPragy(y, zona):
    yConvert = convertire(y, zona, "y")
    prag = round(random.random(), 3)
    if yConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{y} {zona["name"]} \n")
        verificare_nr_puncte()
    else:
        y = alege_valoarea_pt_coord()
        verifPragy(y, zona)

def verifPragx(x,zona):
    xConvert = convertire(x, zona, "x")
    prag = round(random.random(), 3)
    if  xConvert > prag:
        with open(file_name, 'a') as f:
            f.write(f"{x} ")
        coordy = alege_valoarea_pt_coord()
        verifPragy(coordy, zona)
    else:
        x = alege_valoarea_pt_coord()
        verifPragx(x,zona)

def generareCentroizi():
    k = nrOfCentroizi
    while True:
        if k >0:
            with open(centroizi_file_name, 'a') as f:
                f.write(f"{randint(-300,300)} {randint(-300,300)} \n")
            k = k - 1
        else: break

def calcululSimilaritatii(coordXintrare, coordYintrare):
    dist_min = float('inf')
    closest_centroid = None
    counter = 1
    with open(centroizi_file_name, 'r') as f:
        for linie in f:
            coordonate = linie.split()
            distanta = (math.sqrt((coordonate[0] - coordXintrare) ** 2 + (coordonate[1] - coordYintrare) ** 2))
            if distanta < dist_min:
                dist_min = distanta
                closest_centroid = (coordonate[0], coordonate[1], counter)
            counter = counter + 1
    return closest_centroid

def parcurgerePuncte():
    closest_centroid = []
    with open(file_name, 'r') as f:
        for linie in f:
            coordonate = linie.split()
            coordx = coordonate[0]
            coordy = coordonate[1]
            centroid = calcululSimilaritatii(coordx, coordy)
            centroidID = centroid[3]
            closest_centroid. append({"coordx " : coordx, "coordy ": coordy,"centroidID ": centroidID})
    return closest_centroid

def grupareDupaCentroid(closest_centroid):
    grupat_dupa_centroid = {}
    for lista in closest_centroid:
        centroid = lista["centroidID"]
        grupat_dupa_centroid[centroid].append(lista)
    return grupat_dupa_centroid

def calculCentruDeGreutate(grupat_dupa_centroid):
    centrul_de_greutate = []
    for centroizi, lista in grupat_dupa_centroid.items():
        suma_Coordx = sum(centroid["coordx"] for centroid in centroizi )
        suma_Coordy = sum(centroid["coordy"] for centroid in centroizi)
        centrul_de_greutatex = suma_Coordx/nrOfCentroizi
        centrul_de_greutatey = suma_Coordy/nrOfCentroizi
        centrul_de_greutate[centroizi] = (centrul_de_greutatex, centrul_de_greutatey)
    return dict(sorted(centrul_de_greutate.items()))

def mutare_centroizi(centru_de_greutate):
    counter = 1
    x=0
    y=1
    with open(centroizi_file_name, 'r') as f:
        for linie in f:
            linie = linie.split()
            linie[x] = centru_de_greutate[counter][0]
            linie[y] = centru_de_greutate[counter][1]
            counter = counter + 1
def functiaDeConvergenta():



#Algoritm Generare puncte
Zona = random.choice([zona1, zona2, zona3])
x = alege_valoarea_pt_coord()
verifPragx(x,Zona)

#Algoritmul k-Means
generareCentroizi()
closest_centroid_list = parcurgerePuncte()
lista_centroizi_grupati = grupareDupaCentroid(closest_centroid_list)
lista_centre_de_greutate = calculCentruDeGreutate(lista_centroizi_grupati)
mutare_centroizi(lista_centre_de_greutate)


# # AFISARE generarea setului de date
# with open(file_name , 'r') as f:
#     for linie in f:
#         coordonate = linie.split()
#         X.append(float(coordonate[0]))
#         Y.append(float(coordonate[1]))
#         zona = coordonate[2]
#         culori.append(culori_zona[zona])
#
# # Desenăm punctele pe grafic
# plt.scatter(X,  Y, c=culori, s=1)
#
# # Etichete și titlu pentru grafic
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.title("Punctele colorate în funcție de zona")
# plt.axhline(0,color = 'black', linewidth = 0.9)
# plt.axvline(0,color = 'black', linewidth = 0.9)
# # Afișăm graficul
# plt.show()

