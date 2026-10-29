import argparse
import sys
from pathlib import Path

from paths import (
    DAYS_ABB,
    MONTHS,
    TIMES_ABB,
    build_paths,
    create_files,
    expand_day_range,
    read_files
)

def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Skrypt do tworzenia i odczytu plików z danymi (Dane.csv, Dane.json)\n"
            "w strukturze katalogów: <root> / miesiąc / dzień_tygodnia / pora_dnia.\n\n"
            "Zasady działania:\n"
            "  - Miesiące (-m) i zakresy dni (-d) są łączone parami po pozycji (1. z 1., 2. z 2. itd.).\n"
            "    Aby podać kilka zakresów dla jednego miesiąca, powtórz ten miesiąc na liście -m.\n"
            "  - Zakresy dni mogą przechodzić przez weekend (np. pt-pn oznacza: pt, sb, nd, pn).\n"
            "  - Pory dnia (-p) przypisywane są kolejno do dni po rozwinięciu zakresów.\n"
            "    Brakujące pory otrzymują domyślnie wartość 'rano'. Nadmiar pór powoduje błąd.\n"
            "  - W trybie tworzenia (-t) istniejące pliki są domyślnie pomijane (użyj --force, by nadpisać).\n"
            "  - W trybie odczytu (-o) program wypisuje sumę kolumny 'Czas' dla wierszy z Model == 'A'\n"
            "    (osobno dla każdego pliku oraz sumę łączną). Brak pliku przerywa program z kodem 1."
        ),
        epilog=(
            "Przykłady:\n"
            "  # Utworzenie plików Dane.csv i Dane.json w katalogu ./dane:\n"
            "  python skrypt.py -m styczeń luty -d pn-wt pt -p r w -t -c -j --root ./dane\n\n"
            "  # Odczyt utworzonych plików CSV i JSON z katalogu ./dane:\n"
            "  python skrypt.py -m styczeń luty -d pn-wt pt -p r w -o -c -j --root ./dane"
        ),
        # Zachowuje podział na linie w description oraz epilog
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    req_group = parser.add_argument_group('argumenty wymagane')
    req_group.add_argument(
        '-m', 
        '--miesiące',
        nargs='+',
        dest='months',
        metavar='MIESIĄC',
        required=True,
        type=str.lower, # automatyczna normalizacja argumentów 
        help=(
            f"Lista miesięcy (tyle samo co zakresów dni w -d). "
            f"Dozwolone: {', '.join(MONTHS)}"
        )
    )

    req_group.add_argument(
        '-d',
        '--dni',
        nargs='+', 
        dest='days',
        metavar='ZAKRES',
        required=True, 
        type=str.lower,
        help=(
            "Pojedyncze dni lub zakresy dni (np. pt, pn-cz, pt-pn) odpowiadające kolejnym miesiącom. "
            f"Dozwolone skróty: {', '.join(DAYS_ABB.keys())} (lub pełne nazwy dni)"
        )
    )

    mode_group = parser.add_argument_group('tryb działania (wymagany dokładnie jeden z dwóch)')
    # Wykluczające się flagi wymuszają świadomy wybór dokładnie jednego trybu
    mode_mutex = mode_group.add_mutually_exclusive_group(required=True)
    mode_mutex.add_argument(
        '-t', 
        '--tworzenie',
        action='store_true', 
        dest='create', 
        help='Tworzenie struktury katalogów i plików z losowymi danymi'
    )
    mode_mutex.add_argument(
        '-o', 
        '--odczyt',
        action='store_true', 
        dest='read', 
        help='Odczyt plików i sumowanie wartości "Czas" dla Model == "A"'
    )

    opt_group = parser.add_argument_group('argumenty opcjonalne')
    opt_group.add_argument(
        '-p', 
        '--pory',
        nargs='*', 
        dest='times', 
        metavar='PORA',
        type=str.lower, 
        help=(
            "Pory dnia przypisywane kolejno do wygenerowanych dni. "
            "Brakujące przyjmują wartość 'rano' (nadmiar powoduje błąd). "
            f"Dozwolone: {', '.join(TIMES_ABB.keys())}, {', '.join(TIMES_ABB.values())}"
        ), 
        default=[]
    )

    opt_group.add_argument(
        '--root', 
        default=Path('.'), 
        dest='root', 
        type=Path,
        metavar='KATALOG',
        help='Katalog bazowy struktury (dla tworzenia i odczytu), domyślnie bieżący (".")', 
    )

    opt_group.add_argument(
        '--force', 
        action='store_true',
        dest='force', 
        help='Wymuś nadpisanie istniejących plików (działa tylko w trybie tworzenia -t)'
    )

    opt_group.add_argument(
        '-j', 
        '--json',
        action='store_true', 
        dest='json', 
        help='Obsługa formatu JSON (Dane.json); można łączyć z -c'
    )

    opt_group.add_argument(
        '-c', 
        '--csv',
        action='store_true',
        dest='csv', 
        help='Obsługa formatu CSV (Dane.csv). Domyślny format, gdy nie podano -c ani -j; można łączyć z -j'
    )

    return parser

def validate_and_normalize_args(parser, args):
    if len(args.months) != len(args.days):
        parser.error('liczba miesięcy musi być równa liczbie zakresów dni')

    if args.force and not args.create:
        parser.error("flaga --force może być używana tylko w trybie tworzenia (-t)")

    for m in args.months:
        if m not in MONTHS:
            parser.error(f'nieprawidłowy miesiąc: {m}, dozwolone {", ".join(MONTHS)}')

    total_days = 0
    # Akceptujemy zarówno skróty (pn..nd), jak i pełne nazwy dni tygodnia
    valid_days = set(DAYS_ABB.keys()) | set(DAYS_ABB.values())
    normalized_days = []

    for d in args.days:
        parts = d.split('-')
        if not (1 <= len(parts) <= 2):
            parser.error(f'niepoprawny zakres dni: {d}')

        for p in parts:
            if p not in valid_days:
                parser.error(f'niepoprawny dzień: {p}, dozwolone {", ".join(DAYS_ABB.keys())}, {", ".join(DAYS_ABB.values())}')

        # Po walidacji zamieniamy np. ['pn', 'wt'] -> 'poniedziałek-wtorek'
        normalized_days.append('-'.join(DAYS_ABB.get(p, p) for p in parts))
        total_days += len(expand_day_range(d))

    args.days = normalized_days

    valid_times = set(TIMES_ABB.keys()) | set(TIMES_ABB.values())
    normalized_times = []

    for t in args.times:
        if t not in valid_times:
            parser.error(f'niepoprawna pora {t}, dozwolone {", ".join(TIMES_ABB.keys())}, {", ".join(TIMES_ABB.values())}')

        # Zamiana skrótów 'r'/'w' na pełne nazwy katalogów 'rano'/'wieczór'
        normalized_times.append(TIMES_ABB.get(t, t))

    args.times = normalized_times

    if len(args.times) > total_days:
        parser.error(f'za dużo pór dnia ({len(args.times)}) w stosunku do liczby dni ({total_days})')

def get_formats(args):
    formats = []

    if args.json:
        formats.append('json')
    if args.csv or not formats:
        formats.append('csv')

    return formats

def main():
    parser = build_parser()
    args = parser.parse_args()
    validate_and_normalize_args(parser, args)
    formats = get_formats(args)

    # Błędy I/O (np. brak pliku przy odczycie) oraz błędy walidacji danych (ValueError)
    # są obsługiwane centralnie i kończą program z kodem wyjścia 1
    try:
        rel_paths = build_paths(args.months, args.days, args.times)
        # build_paths zwraca ścieżki względne poziomu 3 – doklejamy katalog bazowy --root
        full_paths = [args.root / p for p in rel_paths]
        
        if args.create:
            create_files(full_paths, formats, args.force)
        else:
            read_files(full_paths, formats)
    except (OSError, ValueError) as e:
        print(f'błąd podczas wykonywania operacji: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()