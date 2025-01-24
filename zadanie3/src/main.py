import csv
import matplotlib.pyplot as plt

def odchylenieStandardowe(data3, kolumna):
    return (wariancja(data3, kolumna))**0.5

def wariancja(data3, kolumna):
    n = len(data3)
    licznik = 0.0
    srednia = sredniaArytmetyczna(data3, kolumna)

    for row in data3:
        licznik += ((float(row[kolumna]) - srednia) ** 2)
    return licznik / (n - 1)

def sredniaArytmetyczna(data3, kolumna):
    count = 0
    for i in range(len(data3)):
        count += float(data3[i][kolumna])
    return count / len(data3)

def standaryzacjaDanych(data3):

    liczbaKolumn = len(data3[0]) - 1  
    srednie = []
    odchylenia = []

    for kolumna in range(liczbaKolumn):
        srednia = sredniaArytmetyczna(data3, kolumna)
        odchylenie = odchylenieStandardowe(data3, kolumna)
        srednie.append(srednia)
        odchylenia.append(odchylenie)

    standaryzowane = []
    for row in data3:
        nowyWiersz = []
        for kolumna in range(liczbaKolumn):
            if odchylenia[kolumna] != 0:
                nowyWiersz.append((row[kolumna] - srednie[kolumna]) / odchylenia[kolumna])
            else:
                nowyWiersz.append(0)  
        nowyWiersz.append(row[-1])  
        standaryzowane.append(nowyWiersz)

    return standaryzowane, srednie, odchylenia

def standaryzacjaPunktu(punkt, srednie, odchylenia):
    
    standaryzowanyPunkt = []
    for i in range(len(punkt) - 1): 
        if odchylenia[i] != 0:
            standaryzowanyPunkt.append((punkt[i] - srednie[i]) / odchylenia[i])
        else:
            standaryzowanyPunkt.append(0) 
    
    standaryzowanyPunkt.append(punkt[-1])  
    return standaryzowanyPunkt

def odlegloscEuklidesowa(punkt1, punkt2):
    odleglosc = 0
    for i in range(len(punkt1)-1):
        odleglosc += (punkt1[i] - punkt2[i]) ** 2

    return odleglosc ** 0.5

def algorytmKNN(k, punkt, data3, liczbaCech):

    gatunki = [0, 1, 2]
    standaryzowaneDane, srednieDlaPunktu, odchyleniaDlaPunktu = standaryzacjaDanych(data3)
    standaryzowanyPunkt = standaryzacjaPunktu(punkt, srednieDlaPunktu, odchyleniaDlaPunktu)

    wybraneDaneTreningowe = [[punktTreningowy[i] for i in liczbaCech] + [punktTreningowy[-1]] for punktTreningowy in standaryzowaneDane]
    wybranyPunkt = [standaryzowanyPunkt[i] for i in liczbaCech] + [standaryzowanyPunkt[-1]]

    etykiety = [punkt[-1] for punkt in wybraneDaneTreningowe]
    odleglosci = []

    for punktTreningowy in wybraneDaneTreningowe:
        odleglosci.append(odlegloscEuklidesowa(wybranyPunkt, punktTreningowy))
    odleglosci_etykiety = list(zip(odleglosci, etykiety))
    odleglosci_etykiety.sort(key = lambda x: x[0])
     
    while k>0:
        NN = odleglosci_etykiety[:k]
        etykietyNN = [sasiad[1] for sasiad in NN]
        setosa = etykietyNN.count(0)
        versicolor = etykietyNN.count(1)
        virginica = etykietyNN.count(2)
        liczbyWystapien = [setosa, versicolor, virginica]

        if liczbyWystapien.count(max(liczbyWystapien)) ==1:
            return gatunki[liczbyWystapien.index(max(liczbyWystapien))]
        else:
            k -= 1

sciezkaTrain = "zadanie3/data3_train.csv"
with open(sciezkaTrain) as file:
    data = [row for row in csv.reader(file)]
dataTrain = [[float(value) for value in row] for row in data[0:]]

sciezkaTest = "zadanie3/data3_test.csv"
with open(sciezkaTest) as file:
    data = [row for row in csv.reader(file)]
dataTest = [[float(value) for value in row] for row in data[0:]]

#wszystkie 4 cechy
najlepszeK = None
najlepszaDokladnosc = 0
najlepszaMacierzPomylek = None
dokladnosci = []
wartosciK = list(range(1,16))

for k in range (1,16):
    poprawne=0
    macierzPomylek = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(len(dataTest)):
        
        punkt = dataTest[i]
        etykietaPrawdziwa = int(round(dataTest[i][-1])) 
        etykietaZwrocona = int(round(algorytmKNN(k, punkt, dataTrain, [0, 1, 2, 3])))  

        if etykietaZwrocona==etykietaPrawdziwa:
            poprawne += 1
        
        macierzPomylek[etykietaPrawdziwa][etykietaZwrocona] += 1
    dokladnosc = poprawne / len(dataTest)
    dokladnosci.append(dokladnosc*100)
        
    if dokladnosc > najlepszaDokladnosc:
        najlepszaDokladnosc = dokladnosc
        najlepszeK = k
        najlepszaMacierzPomylek = macierzPomylek

print(f"\nNajlepsze k dla wszystkich cech: {najlepszeK}")
print(f"Skuteczność: {najlepszaDokladnosc * 100:.2f}%")
print("Macierz pomyłek dla najlepszego k:")
for row in najlepszaMacierzPomylek:
    print(row)

plt.bar(wartosciK, dokladnosci, color='#274C3B')
plt.xlabel('Liczba sąsiadów, wartość (k)', fontsize=14)
plt.ylabel('Dokładność (%)', fontsize=14)
plt.title('Dokładność dla różnych wartości k w k-NN dla 4 cech', fontsize=16)
plt.ylim(95, 100.1) 
plt.yticks([i / 10 for i in range(950, 1005, 5)], fontsize=12)
plt.xticks(range(1, 16), fontsize=12)
plt.show()

# po 2 cechy
cechyOpis = ["długości działki kielicha", "szerokości działki kielicha", "długości płatka", "szerokości płatka"]

for cecha1, cecha2 in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
    najlepszeK = 0
    najlepszaDokladnosc = 0
    najlepszaMacierzPomylek = None
    dokladnosci = []
    wartosciK = list(range(1,16))
    for k in range (1,16):
        poprawne=0
        macierzPomylek = [[0 for _ in range(3)] for _ in range(3)]
        cechy = [cecha1, cecha2]

        for i in range(len(dataTest)):
            
            punkt = dataTest[i]
            etykietaPrawdziwa = int(round(dataTest[i][-1]))
            etykietaZwrocona = int(round(algorytmKNN(k, punkt, dataTrain, cechy)))
            if etykietaZwrocona==etykietaPrawdziwa:
                poprawne += 1

            macierzPomylek[etykietaPrawdziwa][etykietaZwrocona] += 1
        dokladnosc = poprawne / len(dataTest)
        dokladnosci.append(dokladnosc*100)
        
        if dokladnosc > najlepszaDokladnosc:
            najlepszaDokladnosc = dokladnosc
            najlepszeK = k
            najlepszaMacierzPomylek = macierzPomylek

    print(f"\nNumery cech: {cecha1, cecha2}")
    print(f"Najlepsze k: {najlepszeK}")
    print(f"Skuteczność: {najlepszaDokladnosc * 100:.2f}%")
    print("Macierz pomyłek dla najlepszego k:")
    for row in najlepszaMacierzPomylek:
        print(row)

    plt.bar(wartosciK, dokladnosci, color='#274C3B')
    plt.xlabel('Liczba sąsiadów, wartość (k)', fontsize=14)
    plt.ylabel('Dokładność (%)', fontsize=14)
    plt.title(f'Dokładność dla różnych wartości k w k-NN \n dla {cechyOpis[cecha1]} i {cechyOpis[cecha2]}', fontsize=16)
    if (cecha1 == 0 and cecha2 == 1):
        plt.ylim(70, 87.1) 
        plt.yticks([i / 10 for i in range(700, 880, 10)], fontsize=12)
    else: 
        plt.ylim(90, 100.1) 
        plt.yticks([i / 10 for i in range(900, 1005, 10)], fontsize=12)
    plt.xticks(range(1, 16), fontsize=12)
    plt.show()