### Instrukcja dla zespołu: Jak pobrać repozytorium i dodać swoją część przez Pull Request

Każda osoba pracuje wyłącznie nad swoim plikiem (`paths.py` dla Osoby 2, `csv_io.py` dla Osoby 3, `json_io.py` dla Osoby 4).

#### 1. Sklonuj repozytorium (jeśli robisz to pierwszy raz)

Otwórz terminal w folderze, gdzie trzymasz projekty, i wpisz:

```bash
git clone <URL_TWOJEGO_REPOZYTORIUM>
cd <NAZWA_KATALOGU_REPOZYTORIUM>

```

*(Jeśli repozytorium już masz sklonowane, upewnij się, że stoisz na gałęzi `main` i pobierz najnowszy stan komendą: `git checkout main` oraz `git pull origin main`)*.

#### 2. Stwórz nową gałąź (branch) dla swojego zadania

Nigdy nie pracujemy bezpośrednio na gałęzi `main`. Utwórz nową gałąź odpowiadającą Twojej roli:

* **Osoba 2**: `git checkout -b feature/paths`
* **Osoba 3**: `git checkout -b feature/csv-io`
* **Osoba 4**: `git checkout -b feature/json-io`

Polecenie `checkout -b` tworzy nową gałąź i od razu na nią przełącza.

#### 3. Zaimplementuj kod

Otwórz projekt w swoim edytorze (np. VS Code, PyCharm). Wypełnij funkcje oznaczone komentarzami `# FIXME` w przypisanym do Ciebie pliku (`paths.py`, `csv_io.py` lub `json_io.py`).

#### 4. Zapisz zmiany i wyślij je na GitHuba

Gdy skończysz pisać i przetestujesz swój moduł:

1. Sprawdź zmodyfikowane pliki:
```bash
git status

```


2. Dodaj swój plik do zapisu:
```bash
git add <nazwa_twojego_pliku.py>

```


3. Zrób commit z jasnym opisem:
```bash
git commit -m "Implementacja zapisu i odczytu csv"

```


4. Wyślij gałąź na serwer GitHuba:
```bash
git push -u origin <nazwa-twojej-gałęzi>

```


*(np. `git push -u origin feature/csv-io`)*.

#### 5. Otwórz Pull Request na stronie GitHuba

1. Wejdź na stronę repozytorium na GitHubie w przeglądarce.
2. Na samej górze pojawi się żółty pasek informujący o nowo wypchniętej gałęzi z przyciskiem **Compare & pull request** – kliknij go.
*(Jeśli paska nie ma, wejdź w zakładkę **Pull requests** $\rightarrow$ kliknij zielony przycisk **New pull request** $\rightarrow$ wybierz jako `compare` swoją gałąź)*.
3. Wpisz krótki tytuł i opis tego, co zostało zrobione.
4. Kliknij zielony przycisk **Create pull request**.

#### 6. Akceptacja (Merge)

Właściciel repozytorium lub inny członek grupy wchodzi w zakładkę **Pull requests**, przegląda zmiany w zakładce **Files changed** i klika zielony przycisk **Merge pull request** $\rightarrow$ **Confirm merge**. Kod z gałęzi trafia wtedy na oficjalny `main`.

#### 7. Aktualizacja lokalnego `main` po scaleniu

Gdy czyjś Pull Request zostanie zmergowany na GitHubie, każdy w zespole powinien zaktualizować swój lokalny kod:

```bash
git checkout main
git pull origin main

```