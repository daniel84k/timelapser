import subprocess
import re

def get_available_iso_values():
    """
    Zwraca listę dostępnych wartości ISO jako (int, string).
    Przykład: (800, "800")
    """
    result = subprocess.run(
        ["gphoto2", "--get-config", "iso"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print("❌ Nie można pobrać konfiguracji ISO.")
        return []

    choices = []
    pattern = r"Choice: \d+ (\d+)"

    for line in result.stdout.splitlines():
        match = re.search(pattern, line)
        if match:
            val_str = match.group(1)
            try:
                val = int(val_str)
                choices.append((val, val_str))
            except ValueError:
                continue

    return choices

def set_closest_iso(target_iso: int, max_iso: int = 1600):
    """
    Dobiera i ustawia najbliższą możliwą wartość ISO ≤ max_iso.
    """
    choices = get_available_iso_values()
    choices = [c for c in choices if c[0] <= max_iso]

    if not choices:
        print(f"❌ Brak dostępnych wartości ISO ≤ {max_iso}")
        return

    closest = min(choices, key=lambda x: abs(x[0] - target_iso))
    print(f"✅ Ustawiam ISO: {closest[0]}")
    
    subprocess.run(["gphoto2", "--set-config", f"iso={closest[1]}"])

