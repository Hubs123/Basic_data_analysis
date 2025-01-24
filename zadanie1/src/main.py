import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# sekcja ogólna - funkcje matematyczne 
def sredniaArytmetyczna(data1, kolumna):
    count = 0
    sum = 0

    for i in range(len(data1)):
        sum += 1
        count += float(data1[i][kolumna])
        
    return count / sum

def odchylenieStandardowe(data1, kolumna):
   
    return np.sqrt(wariancja(data1, kolumna))

def mediana(data1, kolumna):
    tabela = []
    for i in data1:
        tabela.append(float(i[kolumna]))
        
    tabela.sort()
    
    if len(tabela) % 2 == 0:
        return (tabela[(len(tabela) // 2) - 1] + tabela[len(tabela) // 2]) / 2
    else:
        return tabela[len(tabela) // 2]

def q1(data1, kolumna):
    tabela = []
    for i in data1:
        tabela.append(float(i[kolumna]))
        
    tabela.sort()
    
    if len(tabela) % 4 == 1:
        return tabela[len(tabela) // 4]
    else:
        return (tabela[(len(tabela) // 4) - 1] + tabela[(len(tabela) // 4)]) / 2

def q3(data1, kolumna):
    tabela = []
    for i in data1:
        tabela.append(float(i[kolumna]))
        
    tabela.sort()
    
    if len(tabela) % 4 == 1:
        return tabela[len(tabela) // 4 * 3]
    else:
        return (tabela[(len(tabela) // 4 * 3) - 1] + tabela[(len(tabela) // 4 * 3)]) / 2   

def minimum(data1, kolumna):
    min = float(data1[0][kolumna])
    
    for i in range(1, len(data1)):
        temp = float(data1[i][kolumna])
        if temp < min:
            min = temp
    
    return min

def maksimum(data1, kolumna):
    maks = float(data1[0][kolumna])
    
    for i in range(1, len(data1)):
        temp = float(data1[i][kolumna])
        if temp > maks:
            maks = temp
    
    return maks

def wariancja(data1, kolumna):
    n = len(data1)
    licznik = 0.0
    srednia = sredniaArytmetyczna(data1, kolumna)
    
    for row in data1:
        licznik += ((float(row[kolumna]) - srednia) ** 2)
        
    return licznik / (n - 1)

def kowariancja(data1, kolumnaX, kolumnaY):
    n = len(data1)
    sredniaX = sredniaArytmetyczna(data1, kolumnaX)
    sredniaY = sredniaArytmetyczna(data1, kolumnaY)
    
    licznik = 0.0
    
    for row in data1:
        licznik += (float(row[kolumnaX]) - sredniaX) * (float(row[kolumnaY]) - sredniaY)
        
    return licznik / (n - 1)

def rownanieRegresji(data1, kolumnaX, kolumnaY):
    wariancjaX = wariancja(data1, kolumnaX)
    kowariancjaXY = kowariancja(data1, kolumnaX, kolumnaY)
    sredniaX = sredniaArytmetyczna(data1, kolumnaX)
    sredniaY = sredniaArytmetyczna(data1, kolumnaY)
    
    a = kowariancjaXY / wariancjaX
    b = sredniaY - a * sredniaX
    
    return a, b

def korelacjaPearsona(data1, kolumnaX, kolumnaY):
    
    return kowariancja(data1, kolumnaX, kolumnaY) / (odchylenieStandardowe(data1, kolumnaX)*odchylenieStandardowe(data1,kolumnaY))

# sekcja zadania 1 - generowanie tabel, histogramów i wykresów do sprawozdania

def Tabela1(data1):
    setosa = 0
    versicolor = 0
    virginica = 0

    for row in data1:
        if row[4] == '0':
            setosa += 1

        elif row[4] == '1':
            versicolor += 1

        elif row[4] == '2':
            virginica += 1

    perSet = (setosa / len(data1)) * 100
    perVer = (versicolor / len(data1)) * 100
    perVir = (virginica / len(data1)) * 100

    tabela = {
        'Gatunek': ['Setosa', 'Versicolor', 'Virginica', 'Razem'],
        'Liczebność (%)': [
            f'{setosa} ({perSet:.1f}%)',
            f'{versicolor} ({perVer:.1f}%)',
            f'{virginica} ({perVir:.1f}%)',
            f'{len(data1)} (100.0%)']
    }

    df = pd.DataFrame(tabela)

    df['Liczebność (%)'] =  df['Liczebność (%)'].astype(str).str.replace('.',',')

    fig,ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    plt.show()
    

def Tabela2(data1):
    
    tabela2 = {
    'Cecha': ['Długość działki kielicha (cm)', 'Szerokość działki kielicha (cm)', 'Długość płatka (cm)', 'Szerokość płatka (cm)'], 
    'Minimum': [f"{minimum(data1, 0):.2f}",
                f"{minimum(data1, 1):.2f}", 
                f"{minimum(data1, 2):.2f}", 
                f"{minimum(data1, 3):.2f}"],
    'Śr. arytm. (± odch. stand.)': [f"{sredniaArytmetyczna(data1, 0):.2f} (±{odchylenieStandardowe(data1, 0):.2f})", 
                                    f"{sredniaArytmetyczna(data1, 1):.2f} (±{odchylenieStandardowe(data1, 1):.2f})", 
                                    f"{sredniaArytmetyczna(data1, 2):.2f} (±{odchylenieStandardowe(data1, 2):.2f})", 
                                    f"{sredniaArytmetyczna(data1, 3):.2f} (±{odchylenieStandardowe(data1, 3):.2f})",],
    'Mediana (Q1 - Q3)': [f"{mediana(data1, 0):.2f} ({q1(data1, 0):.2f} - {q3(data1, 0):.2f})", 
                          f"{mediana(data1, 1):.2f} ({q1(data1, 1):.2f} - {q3(data1, 1):.2f})", 
                          f"{mediana(data1, 2):.2f} ({q1(data1, 2):.2f} - {q3(data1, 2):.2f})", 
                          f"{mediana(data1, 3):.2f} ({q1(data1, 3):.2f} - {q3(data1, 3):.2f})"],
    'Maksimum': [f"{maksimum(data1, 0):.2f}", 
                 f"{maksimum(data1, 1):.2f}", 
                 f"{maksimum(data1, 2):.2f}", 
                 f"{maksimum(data1, 3):.2f}"]
    }

    df = pd.DataFrame(tabela2)

    #zamiana kropek na przecinki
    kolumna_do_zmiany = ['Minimum','Śr. arytm. (± odch. stand.)','Mediana (Q1 - Q3)','Maksimum']

    for kolumna in kolumna_do_zmiany:
        df[kolumna] =  df[kolumna].astype(str).str.replace('.',',')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    
    tabela2 = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    
    tabela2.auto_set_font_size(False) 
    tabela2.set_fontsize(9)
    tabela2.scale(1.25, 1.25)
    
    tabela2.auto_set_column_width(col=list(range(len(df.columns))))
    
    plt.show()
    

# funkcja potrzebna do prawidłowego formatowania histogramów
def setBins(start, koniec):
    tabela = []
    i = start * 10
    while i <= koniec * 10:
        tabela.append(i)
        i += (0.5 * 10)
        
    for j in range (len(tabela)):
        tabela[j] = tabela[j] / 10
        
    return tabela    

def histogram(data1, kolumna, osX, osY, tytul, start, koniec, maksY):
    tabela = []
    for row in data1:
        tabela.append(float(row[kolumna]))
    
    a = setBins(start, koniec)
    
    plt.xlabel(osX)
    plt.ylabel(osY)
    plt.title(tytul)
    
    ax = plt.gca()
    ax.set_ylim([0.0, maksY])

    plt.hist(tabela, bins=a, edgecolor='black')
    plt.show()

def wykresPudelkowy(data1, kolumna, osY, tytul):
    setosa = []
    versicolor = []
    virginica = []
    
    for row in data1:
        if row[4] == '0':
            setosa.append(float(row[kolumna]))

        elif row[4] == '1':
            versicolor.append(float(row[kolumna]))

        elif row[4] == '2':
            virginica.append(float(row[kolumna]))
        
    kolka = dict(markersize=2.5, linestyle='none')
    
    plt.boxplot([setosa, versicolor, virginica], labels=['Setosa', 'Versicolor', 'Virginica'], flierprops=kolka)    
    
    plt.xlabel('Gatunek')
    plt.ylabel(osY)
    plt.title(tytul)

    plt.show()

def wykresPunktowy(data1, kolumnaX, kolumnaY, osX, osY):
    x = []
    y = []
    
    for row in data1:
        x.append(float(row[kolumnaX]))
        y.append(float(row[kolumnaY]))
    
    x = np.array(x)
    y = np.array(y)
    
    a, b = rownanieRegresji(data1, kolumnaX, kolumnaY)
    r = korelacjaPearsona(data1, kolumnaX, kolumnaY)
    
    plt.scatter(x, y)
    
    liniaRegresji = a * x + b
    plt.plot(x, liniaRegresji, color='red')
    
    plt.xlabel(osX)
    plt.ylabel(osY)

    if (b >= 0):
        plt.title(f'r = {r:.2f}; y = {a:.1f}x + {b:.1f}')
    else:
        plt.title(f'r = {r:.2f}; y = {a:.1f}x {b:.1f}')
    
    plt.show()

#otworzenie pliku z danymi o irysach
sciezka = input("Podaj ścieżkę do pliku z danymi: ")
file = open(sciezka)
data = [row for row in csv.reader(file)]
file.close()
data1 = data[0:]

# tabele
Tabela1(data1)
Tabela2(data1)

# długość działki kielicha
histogram(data1, 0, 'Długość (cm)', 'Liczebność', 'Długość działki kielicha', 4.0, 8.0, 35.0)
wykresPudelkowy(data1, 0, 'Długość (cm)', 'Długość działki kielicha')

# szerokość działki kielicha
histogram(data1, 1, 'Szerokość (cm)', 'Liczebność', 'Szerokość działki kielicha', 2.0, 4.5, 70.0)
wykresPudelkowy(data1, 1, 'Szerokość (cm)', 'Szerokość działki kielicha')

# długość płatka
histogram(data1, 2, 'Długość (cm)', 'Liczebność', 'Długość płatka', 1.0, 7.0, 30.0)
wykresPudelkowy(data1, 2, 'Długość (cm)', 'Długość płatka')

# szerokość płatka
histogram(data1, 3, 'Szerokość (cm)', 'Liczebność', 'Szerokość płatka', 0.0, 2.5, 50.0)
wykresPudelkowy(data1, 3, 'Długość (cm)', 'Szerokość płatka')

# wykresy punktowe
wykresPunktowy(data1, 0, 1, 'Długość działki kielicha (cm)', 'Szerokość działki kielicha (cm)')
wykresPunktowy(data1, 0, 2, 'Długość działki kielicha (cm)', 'Długość płatka (cm)')
wykresPunktowy(data1, 0, 3, 'Długość działki kielicha (cm)', 'Szerokość płatka (cm)')
wykresPunktowy(data1, 1, 2, 'Szerokość działki kielicha (cm)', 'Długość płatka (cm)')
wykresPunktowy(data1, 1, 3, 'Szerokość działki kielicha (cm)', 'Szerokość płatka (cm)')
wykresPunktowy(data1, 2, 3, 'Długość płatka (cm)', 'Szerokość płatka (cm)')