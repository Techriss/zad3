from pathlib import Path
from csv_io import read_csv, write_csv
from json_io import read_json, write_json

DAYS_ABB = {
    "pn": "poniedziałek",
    "wt": "wtorek",
    "śr": "środa",
    "cz": "czwartek",
    "pt": "piątek",
    "sb": "sobota",
    "nd": "niedziela"
}

DAYS = list(DAYS_ABB.values())

MONTHS = [
    "styczeń", 
    "luty", 
    "marzec", 
    "kwiecień", 
    "maj", 
    "czerwiec",
    "lipiec", 
    "sierpień", 
    "wrzesień", 
    "październik", 
    "listopad", 
    "grudzień"
]

TIMES_ABB = {
    "r": "rano",
    "w": "wieczór"
}

CSV_NAME = "Dane.csv"
JSON_NAME = "Dane.json"

WRITERS = {"csv": (CSV_NAME, write_csv), "json": (JSON_NAME, write_json)}
READERS = {"csv": (CSV_NAME, read_csv), "json": (JSON_NAME, read_json)}


def normalize_day(day_str):
    return DAYS_ABB.get(day_str, day_str)


def expand_day_range(day_range):
    parts = day_range.split('-')
    if len(parts) == 1:
        return [normalize_day(parts[0])]

    start_day = normalize_day(parts[0])
    end_day = normalize_day(parts[1])

    start_idx = DAYS.index(start_day)
    end_idx = DAYS.index(end_day)

    # Umożliwienie zawijanych przedziałów dni rozbijając przedział na listę dni
    count = (end_idx - start_idx) % 7 + 1
    return [DAYS[(start_idx + i) % 7] for i in range(count)]


def build_paths(months, day_ranges, times):
    """
    Tworzy listę unikalnych ścieżek składających się z miesiąca, dnia i jego
    pory, którą zwracamy bez 'root'.
    Zakłada, że nazwy miesięcy, dni i pór dnia zostały sprawdzone przez skrypt.
    sprawdza jedynie zgodność liczby argumentów.
    Pory przypisujemy po kolei, brakujące dostają "rano".
    """

    if  len(months) != len(day_ranges):
        raise ValueError(f"Liczba miesięcy: {len(months)} nie jest zgodna "
                         f"z liczbą zakresów dni: {len(day_ranges)}")

    time_idx = 0
    paths = []

    for month, day_range in zip(months, day_ranges):

        days = expand_day_range(day_range)

        for day in days:

            if time_idx < len(times):
                time = times[time_idx]

            else:
                time = "rano"

            time_norm = TIMES_ABB.get(time, time)
            time_idx += 1
            path = Path(month) / day / time_norm

            # duplikaty usuwamy dopiero po dodaniu pory, ponieważ wtorek/rano,
            # i wtorek/wieczór to dwie różne ścieżki. Łączenie ich zgubiłoby
            # jedną porę
            if path not in paths:
                paths.append(path)

    if time_idx < len(times):
        raise ValueError(f"Podano zbyt wiele pór dnia {len(times)} "
                         f"w stosunku do liczby dni {time_idx}")

    return paths


def create_files(paths, formats, force=False):
    """
    Zleca zapis danych do podanych ścieżek paths o danych formatach formats.
    Jeśli flaga force=True, nadpisujemy istniejące dane.
    """

    for path in paths:
        for fmt in formats:

            if fmt not in WRITERS:
                raise ValueError(f"Podano nieobsługiwany typ pliku: {fmt}")

            name, write = WRITERS[fmt]
            file_path = path / name

            if file_path.exists() and not force:
                print(f"Plik {file_path} już istnieje, pomijam "
                      f"(jeśli chcesz nadpisać użyj --force)")
                continue

            # Katalog tworzymy tylko wtedy gdy zapisujemy plik,
            # unikamy pustych katalogów
            path.mkdir(parents=True, exist_ok=True)
            write(file_path)


def read_files(paths, formats):
    """
    Zleca odczyt danych z podanych ścieżek paths o danych formatach formats.
    Wypisuje sumy poszczególnych danych i na końcu sumę całkowitą.
    Brak pliku przerywa odczyt, wyjątek łapiemy w 'main'
    Zwracamy sumę całkowitą z plików
    """

    total_sum = 0
    
    for path in paths:
        for fmt in formats:

            if fmt not in READERS:
                raise ValueError(f"Podano nieobsługiwany typ pliku: {fmt}")
            
            name, read = READERS[fmt]
            file_path = path / name
            # Brak pliku jest obsługiwany w 'main'
            result = read(file_path)
            print(f"Plik {file_path}: suma {result}")
            total_sum += result
    
    print(f"Suma całkowita: {total_sum}")
    return total_sum
