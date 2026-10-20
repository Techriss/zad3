import json
import random
from pathlib import Path

MODELS = ["A", "B", "C"]
MAX_VALUE = 1000


def generate_record() -> dict:
    # Czas zapisujemy jako liczbę, bez litery "s" (w csv jest "465s"),
    # bo w json liczba jest naturalniejsza i łatwiej ją potem zsumować;
    # randint obejmuje oba końce, więc zakres to 0–1000 jak w zadaniu
    return {
        "Model": random.choice(MODELS),
        "Wynik": random.randint(0, MAX_VALUE),
        "Czas": random.randint(0, MAX_VALUE)
    }


def write_json(path: Path) -> None:
    # Zawsze nadpisujemy plik i nie tworzymy katalogu: to, czy istniejący
    # plik pominąć, oraz utworzenie katalogu należy do kodu tworzącego ścieżki
    with path.open("w", encoding="utf-8") as f:
        json.dump(generate_record(), f, ensure_ascii=False, indent=2)


def read_json(path: Path) -> int:
    # Brak pliku i uszkodzony json celowo nie są tu obsługiwane: wyjątki
    # przechodzą do main w skrypt.py, który wypisuje komunikat i kończy program
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"{path}: to nie jest słownik")

    if "Model" not in data or "Czas" not in data:
        raise ValueError(f"{path}: brakuje klucza Model albo Czas")

    # Wynik nie jest potrzebny do sumy, więc go nie sprawdzamy:
    # zły Wynik nie powinien przerywać całego odczytu

    czas = data["Czas"]
    # bool jest podklasą int, więc bez drugiego warunku "Czas": true przeszłoby
    if not isinstance(czas, int) or isinstance(czas, bool):
        raise ValueError(f"{path}: czas musi być liczbą całkowitą, a jest: {czas!r}")

    model = data["Model"]
    # bez tego np. "Model": 5 po cichu dawałoby 0 zamiast błędu
    if not isinstance(model, str):
        raise ValueError(f"{path}: model musi być stringiem, a jest: {model!r}")

    if model == "A":
        return czas
    return 0
