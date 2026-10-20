from pathlib import Path
from csv_io import read_csv, write_csv
from json_io import read_json, write_json

DNI_SKRÓT = {
    "pn": "poniedziałek",
    "wt": "wtorek",
    "śr": "środa",
    "cz": "czwartek",
    "pt": "piątek",
    "sb": "sobota",
    "nd": "niedziela"
}

DNI = list(DNI_SKRÓT.values())

MIESIĄCE = [
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

PORY_SKRÓT = {
    "r": "rano",
    "w": "wieczór"
}

CSV_NAZWA = "Dane.csv"
JSON_NAZWA = "Dane.json"

def normalize_day(day_str):
    return DNI_SKRÓT.get(day_str, day_str)

def expand_day_range(day_range):
    parts = day_range.split("-")
    if len(parts) == 1:
        return [normalize_day(parts[0])]

    start_day = normalize_day(parts[0])
    end_day = normalize_day(parts[1])

    start_idx = DNI.index(start_day)
    end_idx = DNI.index(end_day)

    count = (end_idx - start_idx) % 7 + 1
    return [DNI[(start_idx + i) % 7] for i in range(count)]

def build_paths(months, day_ranges, times):
    ### FIXME
    raise NotImplementedError()

def create_files(paths, formats, force = False):
    ### FIXME
    raise NotImplementedError()

def read_files(paths, formats):
    ### FIXME
    raise NotImplementedError()