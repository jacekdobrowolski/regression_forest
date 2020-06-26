Dokumentacja Końcowa
===============================================================

Projekt wykorzystuje algorytm lasu losowego drzew regresyjnych do predykcji szeregu czasowego.
Projekt ma na celu zapoznanie się z działaniem tego modelu i jego specyfiką.

Przygotowanie danych
--------------------------------------------------------------

Aby drzewa miały większą ilość atrybutów do szeregu został dodany drugi szereg przesunięty o jeden kwant czasu.
Jako wartość do przewidzenia na koniec danych została dodana różnica temperatury z obecnej i przyszłej chwili.
Różnice temperatury mają znacznie mniejszy zakres wahań niż temperatury co umożliwia uzyskanie mniejszego błędu drzewom z mniejszą ilością liści.

+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+
| time | compressor | ambient_temp | refrigerator_temp | compressor | ambient_temp | refrigerator_temp | refrigerator_temp |
+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+
|    0 |          1 |         6.50 |              2.00 |        0.0 |         6.35 |              2.18 |              0.01 |
+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+
|   15 |          0 |         6.35 |              2.18 |        0.0 |         6.20 |              2.19 |             -0.51 |
+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+
|   30 |          0 |         6.20 |              2.19 |        1.0 |         6.05 |              1.68 |             -0.18 |
+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+
|   45 |          1 |         6.05 |              1.68 |        1.0 |         5.90 |              1.50 |              0.14 |
+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+
|   60 |          1 |         5.90 |              1.50 |        0.0 |         5.74 |              1.64 |             -0.02 |
+------+------------+--------------+-------------------+------------+--------------+-------------------+-------------------+

Dane testowe to 10% danych losowo wybranych z całego zbioru.

Implementacja
----------------------------------------------------------------

Do implementacji użyłem języka python i bibliotek pandas i numpy.
Cały algorytm znajduje się w module :mod:`random_forest`.
Dzieli się on na dwa pliki jeden implementuje drzewa :mod:`random_forest.tree`,
drugi natomiast las losowy :mod:`random_forest.forest`.

Tworzenie lasu zaczyna się od losowania z powtórzeniami danych do budowy poszczególnych drzew.
Następnie budowane są drzewa na podstawie podanych danych i konfiguracji.
Budowa drzewa jest zaimplementowania rekurencyjnie. Tworzone są węzły i liście zależnie od rozmiaru zbioru danych.
Tworzenie liścia polega na wyliczeniu średniej wartości zmiennej do przewidywania.
tworzenie węzła polega na znalezieniu miejsca podziału które zminimalizuje funkcje kosztu.
W tym przypadku jest to suma kwadratów różnic. Kiedy zostanie wyznaczony najlepszy podział danego zbioru.
Tworzone są liście na podzbiorach.

Implementacja ma pewne ograniczenia. Zmienna dla której uczy się las musi być w ostatniej kolumnie.
Oraz minimalna ilość atrybutów losowanych do tworzenia węzłów musi być większa niż ilość atrybutów 
gdzie mogą wystąpić takie same wartości (np. zmienna boolean) ponieważ może to spowodować że najlepszy
podział dla danego podzbioru nie istnieje. Innym problemem jest powolność częściowo spowodowana złożonością algorytmu,
aby zminimalizować ten problem drzewa budowane są w oddzielnych procesach co pozwala wykorzystać cały procesor.

Eksperymenty
----------------------------------------------------------------

Aby zmniejszyć wpływ losowości danych i budowy lasu każdy eksperyment będzie powtórzony 10 razy i wynik uśredniony.
Jako błąd użyty został średni błąd względny z wszystkich iteracji.
Metoda naiwna przewiduje temperaturę z poprzedniej chwili.
Las przewiduje zmianę temperatury następnie zostaje on zsumowana z obecną temperaturą.

Najpierw zbadam wpływ rozmiaru liścia na błąd na zbiorze testowym.

.. plot:: ../plot1.py

oraz na zbiorze trenującym.
Im mniejszy liść (więcej liści) tym mniejszy błąd. 

.. plot:: ../plot6.py

Jak widać małe rozmiary liścia prowadzą do przetrenowania modelu (błąd na zbiorze trenującym jest mniejszy niż na testowym).

Wpływ ilości losowanych atrybutów

.. plot:: ../plot2.py

Zbyt mała ilość atrybutów prowadzi do słabych podziałów w drzewach co prowadzi do większego błędu.
Natomiast z byt duża ilość prowadzi to do przetrenowania.

Ilość drzew

.. plot:: ../plot3.py

Ilości drzew powyżej 50 nie poprawiają działania algorytmu natomiast znacznie zwalniają jego działanie

Ilość danych w drzewie

.. plot:: ../plot4.py

Większa ilość danych użytych do budowy drzew poprawia wynik.

Wpływ ilości próbek z poprzednich chwili czasu.

.. plot:: ../plot5.py

Użycie większej ilości próbek z poprzednich chwil czasu nie wiele pomaga modelowi.
Może być to spowodowane mniejszą korelacją dalej odległych próbek.

Wnioski
--------------------------------------

Las losowy nie sprawdza się najlepiej w tym zastosowaniu ze względu na obecność dość dobrej metody naiwnej.
