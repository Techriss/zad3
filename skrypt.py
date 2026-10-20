import argparse
import sys
from pathlib import Path

from paths import (
    DNI_SKRÓT,
    MIESIĄCE,
    PORY_SKRÓT,
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
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    req_group = parser.add_argument_group('argumenty wymagane')
    req_group.add_argument(
        '-m', 
        '--miesiące',
        nargs='+',
        dest='miesiące',
        required=True,
        type=str.lower,
        help=f'Miesiące oddzielone spacjami, dozwolone wartości: {", ".join(MIESIĄCE)}'
    )

    req_group.add_argument(
        '-d',
        '--dni',
        nargs='+', 
        dest='dni', 
        required=True, 
        type=str.lower,
        help=f'Dni lub zakresy dni oddzielone spacjami dla każdego miesiąca, np. wt pn-cz sb-nd, dozwolone wartości: {", ".join(DNI_SKRÓT.keys())}, {", ".join(DNI_SKRÓT.values())}'
    )

    mode_group = parser.add_argument_group('tryb działania (wymagany jeden z dwóch)')
    mode_mutex = mode_group.add_mutually_exclusive_group(required=True)
    mode_mutex.add_argument(
        '-t', 
        action='store_true', 
        dest='tworzenie', 
        help='Tryb tworzenia struktury katalogów i plików z danymi'
    )
    mode_mutex.add_argument(
        '-o', 
        action='store_true', 
        dest='odczyt', 
        help='Tryb odczytu danych'
    )

    opt_group = parser.add_argument_group('argumenty opcjonalne')
    opt_group.add_argument(
        '-p', 
        '--pory',
        nargs='*', 
        dest='pory', 
        required=False, 
        type=str.lower, 
        help=f'Pory dnia dla każdego dnia każdego miesiąca oddzielone spacjami, dozwolone wartości: {", ".join(PORY_SKRÓT.keys())}, {", ".join(PORY_SKRÓT.values())}', 
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
    if (len(args.miesiące) != len(args.dni)):
        parser.error('liczba miesięcy musi być równa liczbie zakresów dni')

    for m in args.miesiące:
        if  m not in MIESIĄCE:
            parser.error(f'nieprawidłowy miesiąc: {m}, dozwolone {", ".join(MIESIĄCE)}')

    total_days = 0
    valid_days = set(DNI_SKRÓT.keys()) | set(DNI_SKRÓT.values())

    for d in args.dni:
        parts = d.split('-')
        if not(1 <= len(parts) <= 2):
            parser.error(f'niepoprawny zakres dni: {d}')

        for p in parts:
            if p not in valid_days:
                parser.error(f'niepoprawny dzień: {p}, dozwolone {", ".join(DNI_SKRÓT.keys())}, {", ".join(DNI_SKRÓT.values())}')

        total_days += len(expand_day_range(d))

    valid_times = set(PORY_SKRÓT.keys()) | set(PORY_SKRÓT.values())
    normalized_times = []

    for t in args.pory:
        if t not in valid_times:
            parser.error(f'niepoprawna pora {t}, dozwolone {", ".join(PORY_SKRÓT.keys())}, {", ".join(PORY_SKRÓT.values())}')

        normalized_times.append(PORY_SKRÓT.get(t, t))

    args.pory = normalized_times

    if (len(args.pory) > total_days):
        parser.error(f'za dużo pór dnia ({len(args.pory)}) w stosunku do liczby dni ({total_days})')

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

    rel_paths = build_paths(args.miesiące, args.dni, args.pory)
    abs_paths = [args.root / p for p in rel_paths]

    try:
        if args.tworzenie:
            create_files(abs_paths, formats, args.force)
        else:
            read_files(abs_paths, formats)
    except (OSError, ValueError) as e:
        print(f'błąd podczas wykonywania operacji: {e}', file=sys.stderr)
        sys.exit(1)

        
if __name__ == '__main__':
    main()