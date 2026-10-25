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

    # umożliwienie zawijanych przedziałów dni
    count = (end_idx - start_idx) % 7 + 1
    return [DAYS[(start_idx + i) % 7] for i in range(count)]




# przeczytaj notatki, dodaj komentarze i sprawdz czy rzucasz wyjatki (mozna je troche ulepszyc)
def build_paths(months, day_ranges, times) -> list[Path]:
    """
    Tworzy listę unikalnych ścieżek składających się z miesiąca, dnia i jego pory, 
    podanych funkcji.
    """

    if  len(months) != len(day_ranges):
        raise ValueError(f"Liczba miesięcy: {len(months)} nie jest zgodna" \
        " z liczbą zakresów dni: {len(day_ranges)}, ")

    time_idx = 0
    paths = []

    for month, day_range in zip(months, day_ranges) :

        days = expand_day_range(day_range)

        for day in days:

            if time_idx < len(times):
                time = times[time_idx]
            
            else: 
                time = "rano"

            time_norm = TIMES_ABB.get(time, time)
            time_idx = time_idx + 1
            path = Path(month) / day / time_norm

            if path not in paths:
                paths.append(path)

    if time_idx < len(times):
        raise ValueError(f"Podano zbyt wiele pór dnia")
    
    return paths

def create_files(paths, formats, force = False):
    """
    Zleca zapis danych do podanych ścieżek paths o danych formatach formats, 
    jeśli flaga force = true, nadpisujemy istniejące dane.
    """

    for path in paths:
        for fmt in formats:

            if fmt == "csv":
                file_path = path / CSV_NAME

                if not file_path.exists() or force:
                    path.mkdir(parents = True, exist_ok = True)
                    write_csv(file_path)

            elif fmt == "json":
                file_path = path / JSON_NAME

                if not file_path.exists() or force:
                    path.mkdir(parents = True, exist_ok = True)
                    write_json(file_path)
            else:
                raise ValueError(f"Podano nieobsługiwany typ pliku: {fmt}")

def read_files(paths, formats) -> int:
    """
        Zleca odczyt danych z podanych ścieżek paths o danych formatach formats.

        Wypisuje sumy poszczególnych danych i na końcu sumę całkowitą  
    """

    total_sum = 0
    
    for path in paths:
        for fmt in formats:
    
            if fmt == "csv":
                file_path = path / CSV_NAME
                result = read_csv(file_path)
                print(f"Plik {file_path}: suma {result}")
                total_sum += result
    
            elif fmt == "json":
                file_path = path / JSON_NAME
                result = read_json(file_path)
                print(f"Plik {file_path}: suma {result}")
                total_sum += result
    
            else:
                raise ValueError(f"Podano nieobsługiwany typ pliku: {fmt}")
    
    print(f"Suma całkowita: {total_sum}")
    return total_sum
