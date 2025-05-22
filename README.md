# 📸 Timelapser

**Timelapser** to narzędzie w Pythonie do automatycznego wykonywania zdjęć typu **timelapse** lub **startrails** z dynamicznie dobieranymi parametrami w zależności od położenia Słońca i ustawień użytkownika.

## 🚀 Funkcje

- Automatyczne wyliczanie parametrów ekspozycji na podstawie danych astronomicznych
- Dwa tryby działania:
  - `timelapse` – zdjęcia w równych odstępach z dynamiczną ekspozycją
  - `startrails` – zdjęcia z długim czasem naświetlania i przerwami
- Tryb symulacji (bez robienia zdjęć – zapis do pliku)
- Obsługa różnych lokalizacji i formatów plików
- Lista obsługiwanych ogniskowych i przysłon
- Wsparcie dla zasady 500/600 (smugi gwiazd)

## 🛠️ Wymagania

- Python 3.8+
- Virtualenv (zalecane)

Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

## 🧪 Uruchomienie (przykład)

```bash
python3 main.py --start-time 20:30 --duration 2 --mode timelapse --interval 5 --location location1
```

Tryb startrails:

```bash
python3 main.py --mode startrails --exposure 30 --gap 5 --iso 800 --focal 35 --aperture 2.8
```

Tryb symulacji:

```bash
python3 main.py --simulation --duration 1
```

## ⚙️ Parametry

| Parametr        | Opis |
|-----------------|------|
| `--start-time`  | Godzina rozpoczęcia sesji (np. `22:00`) |
| `--duration`    | Czas trwania sesji (w godzinach) |
| `--mode`        | `timelapse` lub `startrails` |
| `--simulation`  | Symulacja bez robienia zdjęć |
| `--interval`    | Odstęp między zdjęciami (dla timelapse) |
| `--exposure`    | Czas naświetlania (dla startrails) |
| `--gap`         | Przerwa między zdjęciami (dla startrails) |
| `--iso`         | Czułość ISO |
| `--focal`       | Ogniskowa (np. 35 mm) |
| `--aperture`    | Przysłona (np. 2.8) |
| `--rule`        | Reguła 500 lub 600 |
| `--location`    | Lokalizacja (`location1` lub `location2`) |
| `--format`      | Format zdjęć (`raw`, `jpg`, `raw+jpg`) |
| `--output`      | Folder zapisu zdjęć |

## 📝 Przykład działania

```
Max shutter times for each lens with rule 600
 - 14mm: 42.86 s
 - 15mm: 40.00 s
 - 17mm: 35.29 s
...
```

## 🔧 TODO

- Interfejs GUI
- Obsługa dodatkowych lokalizacji i języków
- Wizualizacja harmonogramu ekspozycji

## 📄 Licencja

Projekt na licencji MIT – używaj, rozwijaj i dziel się!
