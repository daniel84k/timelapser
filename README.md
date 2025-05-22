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

