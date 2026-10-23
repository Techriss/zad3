from pathlib import Path
import csv
import random

# Dopuszczalne modele oraz maksymalna wartość wyniku oraz czasu
MODELS = ["A", "B", "C"]
MAX_VALUE = 1000

def generate_record() -> dict:
    # Generuje słownik reprezentujący pojedynczy losowy rekord danych.
    # Czas jest generowany jako liczba z dopisaną literą "s" (np. "465s").

    return {
        "Model": random.choice(MODELS),
        "Wynik": random.randint(0, MAX_VALUE),
        "Czas": f"{random.randint(0, MAX_VALUE)}s"
    }

def write_csv(path: Path) -> None:
    # Plik jest zawsze nadpisywany.

    record = generate_record()
    
    with path.open("w", encoding="utf-8") as f:
        # Zapis nagłówka oraz wiersza danych w formacie: Model; Wynik; Czas;
        f.write("Model; Wynik; Czas;\n")
        f.write(f"{record['Model']} ; {record['Wynik']} ; {record['Czas']};\n")


def read_csv(path: Path) -> int:
    # Brak pliku celowo nie jest tu obsługiwany. 
    # Wyjątki przechodzą do main w skrypt.py, który wypisuje komunikat i kończy program

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        
        rows = []
        for row in reader:
            rows.append(row)

    if len(rows) != 2:
        raise ValueError(f"{path}: plik CSV musi zawierać dokładnie 2 wiersze")

    # Walidacja nagłówka (; jest separatorem, więc trzeba usunąć puste słowo z końca linijki)
    header_raw = rows[0]
    header = []
    for item in header_raw:
        cleaned = item.strip()
        if cleaned:
            header.append(cleaned)

    expected_header = ["Model", "Wynik", "Czas"]
    if header != expected_header:
        raise ValueError(f"{path}: niepoprawny nagłówek CSV, oczekiwano {expected_header}, a jest: {header}")

    # Pobranie wiersza danych (; jest separatorem, więc trzeba usunąć puste słowo z końca linijki)
    data_raw = rows[1]
    data = []
    for item in data_raw:
        cleaned = item.strip()
        if cleaned:
            data.append(cleaned)

    if len(data) != 3:
        raise ValueError(f"{path}: niepoprawna liczba kolumn w wierszu danych")

    model = data[0].strip()
    czas_raw = data[2].strip()

    # Sprawdza czy model jest stringiem
    if not isinstance(model, str):
        raise ValueError(f"{path}: model musi być stringiem, a jest: {model!r}")

    # Czas w pliku CSV musi posiadać literę "s" na końcu (np. "465s")
    if not czas_raw.endswith("s"):
        raise ValueError(f"{path}: czas musi kończyć się literą 's', a jest: {czas_raw!r}")

    # Odcinanie 's'
    czas_str = czas_raw[:-1].strip()

    # Próba konwersji części liczbowej czasu na int
    try:
        czas = int(czas_str)
    except ValueError:
        raise ValueError(f"{path}: czas musi być liczbą całkowitą, a jest: {czas_raw!r}")

    if model == "A":
        return czas
    return 0