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
    return [DAYS[(start_idx + i) % 7] for i in range(count)] # skrótowy zapis tworzenia listy

def build_paths(months, day_ranges, times):
    ### FIXME
    raise NotImplementedError()

def create_files(paths, formats, force = False):
    ### FIXME
    raise NotImplementedError()

def read_files(paths, formats):
    ### FIXME
    raise NotImplementedError()