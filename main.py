import argparse
from run import run_timelapse

def print_max_exposures(rule):
    print("Max shutter times for each lens with rule", rule)
    for focal in [14, 15, 17, 20, 24, 35, 40, 50, 85, 105, 135, 200, 250, 300, 430]:
        print(f" - {focal}mm: {rule / focal:.2f} s")

def main():
    # Rozszerzone listy ogniskowych i przysłon
    AVAILABLE_FOCALS = [14, 15, 17, 20, 24, 35, 40, 50, 85, 105, 135, 200, 250, 300, 430]
    AVAILABLE_APERTURES = [1.0, 1.2, 1.4, 1.8, 2.0, 2.8, 3.5, 4.0, 5.6, 8.0, 11.0, 12.0, 16.0]

    parser = argparse.ArgumentParser(description="Automatyczne fotografowanie timelapse z ustawieniami zależnymi od pozycji Słońca lub stratrails z ręcznymi parametrami.")
    parser.add_argument("--start-time", type=str, help="Godzina rozpoczęcia w formacie HH:MM (24h).")
    parser.add_argument("--duration", type=float, help="Czas trwania sesji (w godzinach).")
    parser.add_argument("--simulation", action="store_true", help="Tryb symulacji – zapisuje parametry do pliku CSV bez robienia zdjęć.")
    parser.add_argument("--mode", choices=['timelapse', 'startrails'], default='timelapse', help="Tryb pracy: 'timelapse' (dynamiczna ekspozycja) lub 'startrails' (ręczne parametry), default = timelapse.")
    parser.add_argument("--interval", type=int, default=1, help="Odstęp między zdjęciami w sekundach (dla timelapse). default = 1s")
    parser.add_argument("--exposure", type=float, help="Czas naświetlania w sekundach (dla startrails).")
    parser.add_argument("--gap", type=float, help="Przerwa między zdjęciami w sekundach (dla startrails).")
    parser.add_argument("--iso", type=int, help="ISO (dla startrails).")
    parser.add_argument("--focal", type=int, choices=AVAILABLE_FOCALS, default=35,
                        help=f"Długość ogniskowej obiektywu w mm. (default = 35mm) Dostępne: {AVAILABLE_FOCALS}")
    parser.add_argument("--aperture", type=float, choices=AVAILABLE_APERTURES, default=2.0,
                        help=f"Przysłona obiektywu (default = f/2). Dostępne: {AVAILABLE_APERTURES}")
    parser.add_argument("--rule", type=int, choices=[500, 600], default=600, help="Reguła smug gwiazd (500 lub 600, default 600).")
    parser.add_argument("--location", choices=['location2', 'location1'], default='location2', help="Lokalizacja zdjęć (wpływa na położenie Słońca) default = location2 .")
    parser.add_argument("--format", choices=["raw", "jpg", "raw+jpg"], default="raw", help="Format zapisu zdjęć (sterowany z poziomu aparatu).")
    parser.add_argument("--output", type=str, default=".", help="Ścieżka docelowa do zapisu zdjęć (domyślnie bieżący katalog).")

    args = parser.parse_args()
    print_max_exposures(args.rule)
    run_timelapse(args)

if __name__ == "__main__":
    main()

