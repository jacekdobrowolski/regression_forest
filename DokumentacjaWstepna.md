# Dokumentacja wstępna UM

**Temat:**
Algorytm maszynowego uczenia się w zastosowaniu do predykcji wartości szeregu czasowego. Zadanie polega na przewidywaniu temperatury w chłodziarce w zależności od temperatury zewnętrznej i stanu agregatu.

<!-- Zawrzeć precyzyjny opis algorytmów, które będą wykorzystane, wraz z przykładowymi obliczeniami. Na podstawie tego opisu nie znający tematyki przedmiotu programista powinien być w stanie wykonać poprawną implementację. -->
## Opis Algorytmu

W projekcie planuje wykorzystać algorytm lasu losowego drzew regresyjnych.

### Dane

Najpierw należy rozdzielić dane na dane trenujące i dane testowe. Ostatnie 10% danych przeznaczę na testy. Reszta danych będzie podzielona na mniejsze fragmenty na podstawie których będą tworzone poszczególne drzewa regresyjne.Dane zawierają temperaturę wewnątrz chłodziarki, temperaturę zewnętrzną i stan pracy agregatu.

### Tworzenie drzew regresyjnych

Drzewo składa się z węzłów i liści oraz korzenia, pierwszego węzła. Każdy węzeł jest warunkiem decydującym czy wybieramy prawą czy lewą gałąź. Gałęzie zakończone są liśćmi, które reprezentują wynik algorytmu.

Tworzenie drzewa zaczynamy od korzenia. Przebieg tworzenia każdego węzła jest jednakowy. Najpierw sprawdzamy rozmiar zbioru, jeśli jest mniejszy niż dany parametr to węzeł staje się liściem. A jego wartość to średnia wartości szukanej w wybranym zbiorze. Jeśli zbiór jest większy szukamy najlepszego miejsca podziału zbioru. 

Takiego w którym przyrost informacji będzie największy. Liczymy średnią temperaturę wewnątrz urządzenia przed podziałem. Od tej średniej odejmujemy wartość w poszczególnych wierszach sumę tych różnic podniesionych do kwadratu nazywamy SSR. Jest to parametr który chcemy minimalizować podziałem zbioru.

### Tworzenie lasu losowego

Las losowy to zbiór drzew regresyjnych utworzonych na podstawie różnych  danych. Dane dla każdego drzewa są losowane

Wynik przewidziany przez las jest średnią ze wszystkich drzew.
<!-- Przedstawić plan eksperymentów. -->

### Eksperymenty
<!-- Należy wybrać i opisać zbiory danych, które będą używane do badań, należy określić jak zostanie wyłoniony i użyty zbiór trenujący. -->


<p align="right"> Jacek Dobrowolski </p>