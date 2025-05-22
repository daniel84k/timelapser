import subprocess
import logging

def get_battery_level():
    try:
        result = subprocess.run(["gphoto2", "--get-config", "batterylevel"], capture_output=True, text=True, check=False)
        output = result.stdout

        for line in output.splitlines():
            if "Current:" in line:
                battery = line.split("Current:")[1].strip()
                logging.info(f"Battery level: {battery}")
                print(f"🔋 Poziom baterii: {battery}")

                if "%" in battery:
                    level = int(battery.replace("%", "").strip())
                    if level < 20:
                        print("⚠️ Uwaga: Niski poziom baterii!")
                return battery
        print("⚠️ Nie można odczytać poziomu baterii.")
        return None
    except Exception as e:
        print(f"Błąd odczytu baterii: {e}")
        logging.error(f"Battery check error: {e}")
        return None

