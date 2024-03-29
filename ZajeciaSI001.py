# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eoGS4EBDT1VnAooSjj9KU27GT6KKuhel
"""

#J.Czaja, nr indexu 5954, st. zaoczne WSIZ
#POBIERAMY BIBLIOTEKI
import requests
from numpy import cov
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

#1. Napisz funkcję do wczytywania waluty nbp z zadanego okresu (wszystko przekazywane jako parametr)
#    dowolny ze sposobów (plik csv, read_json, dowolne inne)
#BUDUJEMY FUNKCJE Z PARAMETRAMI POBIERANIA DANYCH Z URL
def funkcja_przykladowa(c, a, b):

    eee=c + '/'+a +'/' + b + '/'
    url2 = 'http://api.nbp.pl/api/exchangerates/rates/A/'+eee
    currency_req = requests.get(url2)
    currency_data = currency_req.json()
    return currency_data['rates']

#2. Używając stworzonej funkcji wczytaj dane dwóch wybranych
#przez siebie kursów

# i wypisujemy przykladowe dane dla GBP i CHF z URL

print("Funt brytyjski  ")
print(funkcja_przykladowa('GBP','2019-09-01','2019-09-30'))

print(" ")
print("Frank szwajcarski  ")
print(funkcja_przykladowa('EUR','2019-09-01','2019-09-30'))

#3.Zbadaj wczytane dane za pomocą wybranych poleceń, oczyść jeżeli to konieczne i ustaw indeksy na datę.

#POBIERAMY dane o kursie dla 4 walut, za pomoca ww. funkcji,
#podajemy parametry dla wywolywanej funkcji 
#wybieramy potrzebne kolumny, odpowiednio ustawiamy indeks
#dla kursu kazdej waluty otrzymujemy szereg czasowy(data w jednej "kolumnie", dane w drugiej)
dane_wykres3 = pd.DataFrame.from_dict(funkcja_przykladowa('GBP','2019-09-01','2019-09-30')).set_index(['effectiveDate'])['mid']
dane_wykres4 = pd.DataFrame.from_dict(funkcja_przykladowa('CHF','2019-09-01','2019-09-30')).set_index(['effectiveDate'])['mid']
dane_wykres = pd.DataFrame.from_dict(funkcja_przykladowa('USD','2019-09-01','2019-09-30')).set_index(['effectiveDate'])['mid']
dane_wykres2 = pd.DataFrame.from_dict(funkcja_przykladowa('EUR','2019-09-01','2019-09-30')).set_index(['effectiveDate'])['mid']

#Budujemy tabele i nadajemy nazwy kolumn dla kazdej daty dziennej
df = pd.DataFrame({'USD': dane_wykres}, columns=["USD","EUR","GBP","CHF"])
df['EUR'] = dane_wykres2
df['GBP'] = dane_wykres3
df['CHF'] = dane_wykres4

#pokazujemy pierwsze 7 wierszy szeregów czasowych w zlozonej tabeli
#bez parametru w nawiasie by pokazalo tylko 5
df.head(7)

#pokazujemy ostatnie 5 wierszy szeregów czasowych w zlozonej tabeli
df.tail()

#rysujemy dane szeregow czasowych 4 walut na 1 wykresie
#okreslamy min osi Y dla poprawy widocznoscid danych
#df.plot.area(stacked=False);

df.plot(ylim=(3.8,5))
plt.ylabel('KURS WZGLEDEM PLN')

#Obliczamy srednia kroczaca (usrednianie z 10 wartosci jedna za druga)
#dlatego pierwsze 10 wierszy jest pyste w tabeli wartosci ze srd. kroczaca

print("Obliczamy srednia kroczaca kursu walutowego dla 4 walut")
ma = df.rolling(10).mean()
print(ma)

#Budujemy tabele i filtrujemy lambda kursy mniejsze niz 4.34
#dla USD otrzymujemy tabele bez wartosci liczbowych i jest ciag NaN
dff = pd.DataFrame({'USD': list(filter(lambda x: x>4.34, dane_wykres.to_numpy()))}, columns=["USD","EUR","GBP","CHF"])
dff['EUR'] = list(filter(lambda x: x>4.34, dane_wykres2.to_numpy()))
dff['GBP'] = list(filter(lambda x: x>4.34, dane_wykres2.to_numpy()))
dff['CHF'] = list(filter(lambda x: x>4.34, dane_wykres2.to_numpy()))
print(dff)
print()
#######################################################
#Zastosowanie REDUCE z lambda, mnozenie wartosci kursu, kosmiczne liczby....
#tworzymy ciag dla USD, ale zmniejszamy granice filtrowania do 3.34 dla kursu
#inaczej reduce wyrzuci blad no initial value, bo jest ciag NaN ww. dokonanym filtorwaniu
ba = list(filter(lambda x: x>3.34, dane_wykres.to_numpy()))

from functools import reduce
print ("wynik reduce dla danych kursu USD : " , reduce((lambda x, y: x * y), ba))
#korzystany z odniesien do tablicy danych po filtrowaniu
print ("wynik reduce dla danych kursu EUR : " , reduce((lambda x, y: x * y), dff['EUR']))
print ("wynik reduce dla danych kursu GBP : " , reduce((lambda x, y: x * y), dff['GBP']))
print ("wynik reduce dla danych kursu CHF : " , reduce((lambda x, y: x * y), dff['CHF']))
print()
#######################################################
#podstawowe statystki danych kursow 4 walut, np.min,max, odchylenie, srednia etc.
#df.apply(lambda x: x.describe())
att=(lambda x: x.describe())
print(att(df))
print()
#######################################################

#tworzymy funkcje z lambda
#zabawa w przemnozenie lambda wszystkich kursow 
def fff(num):
    return lambda x: x * num
result1 = fff(20)
result1(df)
print(result1(df))

#Obliczamy korelację Spearmana miedzy kursem GBP i CHF
q=dane_wykres3.corr(dane_wykres4, method= 'spearman')
print("Obliczamy korelację Spearmana miedzy kursem GBP i CHF")
print(q)

#Obliczamy korelacje GBP I CHF, generujemy wykres punktowy
#czyli wykres rozproszenia, aby zbadać związek między tymi dwiema zmiennymi.
#korelacja dotyczy siły badanej współzależności

print("Obliczamy korelacje kursow GBP I CHF, generujemy wykres punktowy(matplotlib)")

#from matplotlib import pyplot
#korelacja na wykresie

plt.scatter(dane_wykres3, dane_wykres4)
plt.ylabel('KURS GBP/PLN')
plt.xlabel('KURS CHF/PLN')
plt.show()
print("Obliczamy korelacje kursow GBP I CHF, generujemy wykres punktowy(seaborn)")

sns.regplot(dane_wykres3, dane_wykres4)
plt.ylabel('KURS GBP/PLN')
plt.xlabel('KURS CHF/PLN')

#ZBUDOWANIE HEATMAP korelacji dla 4 badanych kursow walut
import numpy as np

df = pd.DataFrame({'USD': dane_wykres}, columns=["USD","EUR","GBP","CHF"])
df['EUR'] = dane_wykres2
df['GBP'] = dane_wykres3
df['CHF'] = dane_wykres4
corr=df.corr(method= 'pearson')

print("Budujemy heatmape korelacje kursow USD, EUR, GBP, CHF")

fig, ax = plt.subplots(figsize=(10, 10))
#Generowanie macierzy korelacji wyrazonej kolorami
colormap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=colormap, annot=True, fmt=".2f")

plt.title('HEATMAPa KORELACJI KURSOWYCH WALUT')
plt.xticks(range(len(corr.columns)), corr.columns);
    #Apply yticks
plt.yticks(range(len(corr.columns)), corr.columns)
    #show plot
plt.show()

#generujemy linię regresji dla kursow EUR I USD
#regresja dotyczy charakteru zależności pomiędzy cechami.

plt.figure(figsize=(10,4), dpi=120) # 10 is width, 4 is height

x = np.arange(len(dane_wykres3), dtype=int)
a, b = np.polyfit(x, dane_wykres3, 1)

# matematyka, szkoła średnia
y = a*x+b

x2 = np.arange(len(dane_wykres2), dtype=int)
a2, b2 = np.polyfit(x2, dane_wykres2, 1)

# matematyka, szkoła średnia
y2 = a2*x2+b2

plt.subplot(1,2,1)  #ukladamy 2 wykresy obok siebie
plt.plot(x, y, 'go')
plt.ylabel('KURS GBP/PLN') # nadajmy nazwe osi Y
plt.plot(dane_wykres3)
plt.tight_layout()
plt.xticks((0, 5, 10, 15, 20)) #okreslamy gestosc oznaczen osi X 
plt.xticks(rotation=40)        #zmieniamy nachylenie tekstu pod osia X
plt.subplot(1,2,2)
plt.plot(x2, y2, 'b*')
plt.plot(dane_wykres2)
plt.ylabel('KURS EUR/PLN')

plt.tight_layout()
plt.xticks((0, 5, 10, 15, 20))
plt.xticks(rotation=40)
plt.show()

# REGRESJA, KORELACJA, DYSTRYBUCJA
#regresja dotyczy kształtu zależności pomiędzy cechami.
#scatter matrix czyli tzw.Macierz rozproszenia składa się z kilku par wykresów rozproszenia zmiennych przedstawionych
#w formacie macierzy. Można go użyć do ustalenia, czy zmienne są skorelowane i czy korelacja jest dodatnia czy ujemna.
import seaborn as sns
import pandas as pd
import numpy as np
 
df = pd.DataFrame({'USD': dane_wykres}, columns=["USD","EUR","GBP","CHF"])
df['EUR'] = dane_wykres2
df['GBP'] = dane_wykres3
df['CHF'] = dane_wykres4

#rysowanie wykresow w formie macierzowego zestawienia
g = sns.pairplot(df, kind="reg")
g.fig.suptitle("Histogramy i korelacje USD, EUR, GBP, CHF")
plt.show()



