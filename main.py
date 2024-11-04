import random
from random import randint
import matplotlib.pyplot as plt
import sys
import numpy as np

sys.setrecursionlimit(10000000)

file_name = 'coord_X_coord_Y_index_Zona.txt'
centroizi= "Centroizi.txt"

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

def generareCentroizi():
    with open(centroizi, 'a') as f:
        f.write(f"{randint(1, 10)} {randint} \n")

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


#Algoritm Generare puncte
Zona = random.choice([zona1, zona2, zona3])
x = alege_valoarea_pt_coord()
verifPragx(x,Zona)

# AFISARE
with open(file_name , 'r') as f:
    for linie in f:
        coordonate = linie.split()
        X.append(float(coordonate[0]))
        Y.append(float(coordonate[1]))
        zona = coordonate[2]
        culori.append(culori_zona[zona])

# Desenăm punctele pe grafic
plt.scatter(X,  Y, c=culori, s=1)

# Etichete și titlu pentru grafic
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Punctele colorate în funcție de zona")
plt.axhline(0,color = 'black', linewidth = 0.9)
plt.axvline(0,color = 'black', linewidth = 0.9)
# Afișăm graficul
plt.show()

