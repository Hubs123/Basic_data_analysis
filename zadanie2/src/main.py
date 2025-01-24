import random
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt


# funkcje potrzebne do algorytmu k-srednich
def standaryzacja(data2):
    standaryzowane = []
    liczbaKolumn = len(data2[0])

    for kolumna in range(liczbaKolumn):
        kolumnaWartosci = [float(row[kolumna]) for row in data2]
        srednia = sredniaArytmetyczna(data2, kolumna)
        odchylenie = odchylenieStandardowe(data2, kolumna)

        if odchylenie != 0:
            standaryzowane.append([(x - srednia) / odchylenie for x in kolumnaWartosci])
        else:
            standaryzowane.append([0 for _ in kolumnaWartosci])

    return np.array(standaryzowane).T


def destandaryzacjaKlastrow(klastry, olddata):
    srednie = [sredniaArytmetyczna(olddata, i) for i in range(len(olddata[0]))]
    odchylenia = [odchylenieStandardowe(olddata, i) for i in range(len(olddata[0]))]

    destandaryzowaneKlastry = []

    for klaster in klastry:
        destandaryzowaneKlaster = []
        for punkt in klaster:
            destandaryzowanePunkt = [(punkt[j] * odchylenia[j]) + srednie[j] for j in range(len(punkt))]
            destandaryzowaneKlaster.append(destandaryzowanePunkt)

        destandaryzowaneKlastry.append(destandaryzowaneKlaster)

    return destandaryzowaneKlastry


def destandaryzacjaCentroidow(centroidy, olddata):
    srednie = [sredniaArytmetyczna(olddata, i) for i in range(len(olddata[0]))]
    odchylenia = [odchylenieStandardowe(olddata, i) for i in range(len(olddata[0]))]

    destandaryzowaneCentroidy = []
    for centroid in centroidy:
        destandaryzowaneCentroid = [(centroid[j] * odchylenia[j]) + srednie[j] for j in range(len(centroid))]
        destandaryzowaneCentroidy.append(destandaryzowaneCentroid)

    return destandaryzowaneCentroidy


# funkcje matematyczne
def odchylenieStandardowe(data2, kolumna):
    return np.sqrt(wariancja(data2, kolumna))


def wariancja(data2, kolumna):
    n = len(data2)
    licznik = 0.0
    srednia = sredniaArytmetyczna(data2, kolumna)

    for row in data2:
        licznik += ((float(row[kolumna]) - srednia) ** 2)

    return licznik / (n - 1)


def sredniaArytmetyczna(data2, kolumna):
    count = 0

    for i in range(len(data2)):
        count += float(data2[i][kolumna])

    return count / len(data2)


# algorytm k-srednich
def losowanieCentroidu(data2, k):
    return random.sample(list(data2), k)


def odlegloscPunktuOdCentroidu(punkt, centroid):
    odleglosc = 0
    for i in range(len(punkt)):
        odleglosc += (punkt[i] - centroid[i]) ** 2

    return odleglosc ** 0.5


def przypiszPunktDoKlastra(data2, centroidy):
    klastry = [[] for i in range(len(centroidy))]

    for i in data2:
        minOdleglosc = odlegloscPunktuOdCentroidu(i, centroidy[0])
        najblizszyCentroid = 0
        for j in range(1, len(centroidy)):
            odleglosc = odlegloscPunktuOdCentroidu(i, centroidy[j])
            if odleglosc < minOdleglosc:
                minOdleglosc = odleglosc
                najblizszyCentroid = j
        klastry[najblizszyCentroid].append(i)
    return klastry


def poprawaCentroidow(klastry):
    noweCentroidy = []
    for klaster in klastry:
        centroid = []
        for i in range(len(klaster[0])):
            centroid.append(0)
        for punkt in klaster:
            for i in range(len(punkt)):
                centroid[i] += punkt[i]
        for i in range(len(centroid)):
            centroid[i] /= len(klaster)
        noweCentroidy.append(centroid)
    return noweCentroidy


def wcss(klastry, centroidy):
    wcss = 0
    for klasterIndex in range(len(klastry)):
        klaster = klastry[klasterIndex]
        centroid = centroidy[klasterIndex]
        for punkt in klaster:
            for i in range(len(punkt)):
                wcss += (punkt[i] - centroid[i]) ** 2
    return wcss


def kSrednie(data, k, max_iter=50):
    centroidy = losowanieCentroidu(data, k)
    stareCentroidy = centroidy.copy()
    iteracje = 0
    while iteracje < max_iter:
        iteracje += 1
        klastry = przypiszPunktDoKlastra(data, centroidy)
        centroidy = poprawaCentroidow(klastry)

        if np.array_equal(stareCentroidy, centroidy):
            break

        stareCentroidy = centroidy.copy()

    wcss_value = wcss(klastry, centroidy)
    return klastry, centroidy, wcss_value, iteracje


# wczytanie danych z pliku
sciezka = input("Podaj ścieżkę do pliku z danymi: ")
with open(sciezka) as file:
    data = [row for row in csv.reader(file)]
data2 = [[float(value) for value in row] for row in data[1:]]

# wywolanie algorytmu do wcss
standaryzowaneDane = standaryzacja(data2)

data_list = []
for i in range(2, 11):
    klastry, centroidy, wcss_value, iteracje = kSrednie(standaryzowaneDane, i)
    print(wcss_value)
    data_list.append({
        'k_value': i,
        'liczba iteracji': iteracje,
        'wcss': wcss_value
    })

outputData = pd.DataFrame(data_list)

plt.figure(figsize=(8, 5))
plt.plot(outputData['k_value'], outputData['wcss'], marker='o', color="fuchsia")
plt.xlabel('Liczba klastrów')
plt.ylabel('WCSS')
plt.grid(True, color='Lavender')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(outputData['k_value'], outputData['liczba iteracji'], marker='o', color="fuchsia")
plt.xlabel('Liczba klastrów')
plt.ylabel('Liczba iteracji')
plt.grid(True, color='Lavender')
plt.tight_layout()
plt.show()

klastry, centroidy, wcss_value, iteracje = kSrednie(standaryzowaneDane, 3)

klastry2 = destandaryzacjaKlastrow(klastry, data2)
centroidy2 = destandaryzacjaCentroidow(centroidy, data2)


def wykresKlastry(klastry, centroidy, x_idx, y_idx):
    features = ['Szerokość działki kielicha [cm]', 'Długość działki kielicha [cm]', 'Szerokość płatka [cm]',
                'Długość płatka [cm]']

    colors = ['fuchsia', '#FF5800', '#5579FF']

    plt.figure(figsize=(8, 6))

    for klaster_idx, klaster in enumerate(klastry):
        klaster = np.array(klaster)
        plt.scatter(
            klaster[:, x_idx],
            klaster[:, y_idx],
            color=colors[klaster_idx],
            label=f"Klaster {klaster_idx + 1}",
            alpha=0.6
        )

    centroidy = np.array(centroidy)
    for klaster_idx, centroid in enumerate(centroidy):
        plt.scatter(
            centroid[x_idx],
            centroid[y_idx],
            color=colors[klaster_idx],
            s=100,
            edgecolors='black',
            linewidth=1.5,
            marker='D',
        )

    plt.xlabel(features[x_idx])
    plt.ylabel(features[y_idx])
    plt.tight_layout()
    plt.show()


for x_idx, y_idx in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
    wykresKlastry(
        klastry=klastry2,
        centroidy=np.array(centroidy2),
        x_idx=x_idx,
        y_idx=y_idx
    )

