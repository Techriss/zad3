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
        description='Skrypt do tworzenia i odczytu danych (CSV/JSON) w strukturze katalogów: miesiąc / dzień_tygodnia / pora_dnia.',
        epilog='''Przykład użycia:
                    python skrypt.py -m styczeń luty -d pn-wt pt -p r w -t -c
                    python skrypt.py -m styczeń luty -d pn-wt pt -o -c -j --root ./dane'''
        ,
        formatter_class=argparse.RawDescriptionHelpFormatter # umożliwia m.in. zapis opisów na wiele linii
    )

    req_group = parser.add_argument_group('argumenty wymagane')
    req_group.add_argument(
        '-m', 
        '--miesiące',
        nargs='+',
        dest='months',
        required=True,
        type=str.lower, # automatyczna normalizacja argumentów 
        help=f'Miesiące oddzielone spacjami, dozwolone wartości: {", ".join(MONTHS)}'
    )

    req_group.add_argument(
        '-d',
        '--dni',
        nargs='+', 
        dest='days', 
        required=True, 
        type=str.lower,
        help=f'Dni lub zakresy dni oddzielone spacjami dla każdego miesiąca, np. wt pn-cz sb-nd, dozwolone wartości: {", ".join(DAYS_ABB.keys())}, {", ".join(DAYS_ABB.values())}'
    )

    mode_group = parser.add_argument_group('tryb działania (wymagany jeden z dwóch)')
    mode_mutex = mode_group.add_mutually_exclusive_group(required=True) # umożliwia wybór tylko jednego argumentu z grupy
    mode_mutex.add_argument(
        '-t', 
        action='store_true', 
        dest='create', 
        help='Tryb tworzenia struktury katalogów i plików z danymi'
    )
    mode_mutex.add_argument(
        '-o', 
        action='store_true', 
        dest='view', 
        help='Tryb odczytu danych'
    )

    opt_group = parser.add_argument_group('argumenty opcjonalne')
    opt_group.add_argument(
        '-p', 
        '--pory',
        nargs='*', 
        dest='times', 
        required=False, 
        type=str.lower, 
        help=f'Pory dnia dla każdego dnia każdego miesiąca oddzielone spacjami, dozwolone wartości: {", ".join(TIMES_ABB.keys())}, {", ".join(TIMES_ABB.values())}', 
        default=[]
    )

    opt_group.add_argument(
        '--root', 
        default=Path('.'), 
        dest='root', 
        type=Path,
        help='Katalog docelowy do tworzenia struktury katalogów, domyślnie katalog bieżący', 
    )

    opt_group.add_argument(
        '--force', 
        action='store_true',
        dest='force', 
        help='Flaga wymuszająca nadpisanie istniejących plików'
    )

    opt_group.add_argument(
        '-j', 
        action='store_true', 
        dest='json', 
        help='Twórz pliki JSON'
    )

    opt_group.add_argument(
        '-c', 
        action='store_true',
        dest='csv', 
        help='Twórz pliki CSV, domyślny format'
    )

    return parser

def validate_args(parser, args):
    if (len(args.months) != len(args.days)):
        parser.error('liczba miesięcy musi być równa liczbie zakresów dni')

    for m in args.months:
        if  m not in MONTHS:
            parser.error(f'nieprawidłowy miesiąc: {m}, dozwolone {", ".join(MONTHS)}')

    total_days = 0
    valid_days = set(DAYS_ABB.keys()) | set(DAYS_ABB.values()) # suma zbiorów

    for d in args.days:
        parts = d.split('-')
        if not(1 <= len(parts) <= 2):
            parser.error(f'niepoprawny zakres dni: {d}')

        for p in parts:
            if p not in valid_days:
                parser.error(f'niepoprawny dzień: {p}, dozwolone {", ".join(DAYS_ABB.keys())}, {", ".join(DAYS_ABB.values())}')

        total_days += len(expand_day_range(d))

    valid_times = set(TIMES_ABB.keys()) | set(TIMES_ABB.values())
    normalized_times = []

    for t in args.times:
        if t not in valid_times:
            parser.error(f'niepoprawna pora {t}, dozwolone {", ".join(TIMES_ABB.keys())}, {", ".join(TIMES_ABB.values())}')

        normalized_times.append(TIMES_ABB.get(t, t))

    args.times = normalized_times

    if (len(args.times) > total_days):
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
    validate_args(parser, args)
    formats = get_formats(args)

    rel_paths = build_paths(args.months, args.days, args.times)
    abs_paths = [args.root / p for p in rel_paths] # skrótowy zapis tworzenia listy

    try:
        if args.create:
            create_files(abs_paths, formats, args.force)
        else:
            read_files(abs_paths, formats)
    except (OSError, ValueError) as e:
        print(f'błąd podczas wykonywania operacji: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()