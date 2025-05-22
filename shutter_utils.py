import subprocess
import re

def get_available_shutter_speeds():
    """
    Zwraca listę czasów migawki jako (float, string_z_przecinkiem).
    Przykład: (0.7692, "0,7692")
    """
    result = subprocess.run(
        ["gphoto2", "--get-config", "shutterspeed"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print("❌ Nie można pobrać konfiguracji migawki.")
        return []

    choices = []
    pattern = r"Choice: \d+ ([\d,]+)s"

    for line in result.stdout.splitlines():
        match = re.search(pattern, line)
        if match:
            val_str = match.group(1).replace(",", ".")
            try:
                val = float(val_str)
                choices.append((val, match.group(1)))  # (0.7692, "0,7692")
            except ValueError:
                continue

    return choices

def set_closest_shutter_speed(target_seconds: float, max_shutter: float):
    """
    Dobiera i ustawia najbliższy dostępny czas migawki z listy aparatu,
    ale nie przekracza max_shutter (wynikającego z reguły 500/600).
    """
    choices = get_available_shutter_speeds()
    choices = [c for c in choices if c[0] <= max_shutter]

    if not choices:
        print(f"❌ Brak czasów migawki ≤ {max_shutter:.4f}s (reguła {max_shutter} sekund).")
        return

    closest = min(choices, key=lambda x: abs(x[0] - target_seconds))
    print(f"✅ Ustawiam migawkę: {closest[0]}s ({closest[1]}s)")

    subprocess.run(["gphoto2", "--set-config", f"shutterspeed={closest[1]}s"])

