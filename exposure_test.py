import argparse
import csv
import os
import time
import subprocess
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import elevation
from pytz import timezone

# --- Parametry ---
ISO_VALUES = [100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600]
SHUTTER_SPEEDS = [
    1/4000, 1/3200, 1/2500, 1/2000, 1/1600, 1/1250, 1/1000, 1/800, 1/640, 1/500,
    1/400, 1/320, 1/250, 1/200, 1/160, 1/125, 1/100, 1/80, 1/60, 1/50, 1/40,
    1/30, 1/25, 1/20, 1/15, 1/13, 1/10, 1/8, 1/6, 1/5, 1/4, 0.3, 0.4, 0.5,
    0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.2, 4.0, 5.0, 6.0, 8.0, 10.0, 13.0, 15.0, 20.0, 25.0, 30.0
]
MAX_EXPOSURE_DAY = 1 / 125
AGGRESSIVENESS = {
    "teresin": [0.7, 0.7, 0.7, 0.7],
    "tivoli": [0.5, 0.5, 0.5, 0.5]
}
LOCATIONS = {
    "teresin": ("Europe/Warsaw", 52.2202, 20.4366),
    "tivoli": ("Africa/Windhoek", -23.3167, 17.9333)
}

# --- Funkcje ekspozycji ---
def round_to_nearest(value, options):
    return min(options, key=lambda x: abs(x - value))

def classify_phase(alt):
    if alt > 6: return 0
    elif 0 < alt <= 6: return 1
    elif -6 < alt <= 0: return 2
    elif -12 < alt <= -6: return 2
    elif -18 < alt <= -12: return 3
    else: return 3

def calculate_exposure(alt, aggr_phases, max_exposure_night, apply_gradient=False):
    phase = classify_phase(alt)
    aggressiveness = aggr_phases[phase]

    if alt >= 4:
        factor = max(0.0, -0.1 * (alt - 4) / (90 - 4)) if apply_gradient else 0.0
    elif alt <= -12:
        factor = 1.0
    else:
        factor = (4 - alt) / 16
        factor = min(max(factor, 0.0), 1.0)
        factor = factor ** (1 / aggressiveness)

    target_shutter = MAX_EXPOSURE_DAY + factor * (max_exposure_night - MAX_EXPOSURE_DAY)
    target_iso = ISO_VALUES[0] if factor < 0.5 else ISO_VALUES[0] + (factor - 0.5) * 2 * (ISO_VALUES[-1] - ISO_VALUES[0])

    shutter = round_to_nearest(target_shutter, SHUTTER_SPEEDS)
    iso = round_to_nearest(target_iso, ISO_VALUES)
    return round(shutter, 5), iso

def get_exposure_for_altitude(altitude, focal_length, rule, location, apply_gradient):
    max_exposure_night = rule / focal_length
    aggr_phases = AGGRESSIVENESS.get(location.lower(), [0.9, 0.9, 0.9, 0.9])
    return calculate_exposure(altitude, aggr_phases, max_exposure_night, apply_gradient=apply_gradient)

def get_sun_altitude(lat, lon, dt, tz_str):
    loc = LocationInfo(name="Custom", region="", timezone=tz_str, latitude=lat, longitude=lon)
    return elevation(loc.observer, dt.astimezone(timezone(tz_str)))

def check_battery_level():
    try:
        result = subprocess.run(["gphoto2", "--get-config", "batterylevel"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Current:" in line:
                val = line.split("Current:")[-1].strip().replace("%", "")
                if val.isdigit():
                    level = int(val)
                    print(f"🔋 Poziom baterii: {level}%")
                    if level < 15:
                        print("⚠️ UWAGA: Bateria poniżej 15%!")
    except Exception as e:
        print(f"Błąd odczytu baterii: {e}")

def print_max_exposures():
    print("\n📋 Max shutter times for each lens with rule 500-600")
    focals = [14, 15, 17, 20, 24, 35, 40, 50, 85, 105, 135, 200, 250, 300, 430]
    for focal in focals:
        exp_500 = 500 / focal
        exp_600 = 600 / focal
        if round(exp_500, 2) == round(exp_600, 2):
            print(f" - {focal}mm: {exp_500:.2f} s")
        else:
            print(f" - {focal}mm: {exp_500:.2f}-{exp_600:.2f} s")

# --- Timelapse ---
def run_timelapse(args):
    tz_str, lat, lon = LOCATIONS[args.location]
    tz = timezone(tz_str)
    now = datetime.now(tz)
    end_time = now + timedelta(hours=args.duration)

    folder_name = now.strftime(f"%Y%m%d_%H%M_{args.location}")
    output_dir = os.path.join("output", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n📂 Zdjęcia będą zapisywane do: {output_dir}")

    index = 1
    while datetime.now(tz) < end_time:
        loop_start = time.time()

        current_time = datetime.now(tz)
        alt = get_sun_altitude(lat, lon, current_time, tz_str)
        shutter, iso = get_exposure_for_altitude(alt, args.focal, args.rule, args.location, args.gradient)

        print(f"\n[{index}] {current_time.strftime('%H:%M:%S')} | ALT: {alt:.2f}° | Shutter: {shutter}s | ISO: {iso}")

        shutter_str = f"{shutter:.4f}s".replace(".", ",")

        subprocess.run(["gphoto2", "--set-config", f"iso={iso}"], check=False)
        subprocess.run(["gphoto2", "--set-config", f"shutterspeed={shutter_str}"], check=False)

        filename_base = os.path.join(output_dir, f"IMG_{index:04d}")
        subprocess.run([
            "gphoto2",
            "--capture-image-and-download",
            "--force-overwrite",
            "--filename", f"{filename_base}.%C"
        ], check=False)

        time.sleep(1)  # Opóźnienie na stabilizację aparatu/USB

        if index % 10 == 0:
            check_battery_level()

        index += 1

        elapsed = time.time() - loop_start
        remaining = args.interval - elapsed
        if remaining > 0:
            print(f"⌛ Czekam {int(remaining)}s do kolejnego zdjęcia...")
            time.sleep(remaining)
        else:
            print(f"⚠️ Zdjęcie trwało {int(elapsed)}s, więcej niż interwał ({args.interval}s) — pomijam oczekiwanie.")

# --- Startrails ---
def run_startrails(args):
    if None in (args.exposure, args.gap, args.duration, args.iso):
        print("❌ W trybie startrails wymagane są: --exposure, --gap, --duration, --iso")
        exit(1)

    total_seconds = int(args.duration * 3600)
    total_images = total_seconds // int(args.exposure + args.gap)

    print(f"\n🌌 Startrails Mode")
    print(f"⏱ Ekspozycja: {args.exposure}s | Przerwa: {args.gap}s | ISO: {args.iso} | Czas: {args.duration}h")
    print(f"📸 Zostanie wykonanych: {total_images} zdjęć")
    for fps in [24, 30]:
        video_duration = total_images / fps
        print(f"🎮 Przy {fps} fps: {video_duration:.1f}s ({video_duration/60:.1f} min)")

    tz_str, _, _ = LOCATIONS[args.location]
    tz = timezone(tz_str)
    now = datetime.now(tz)
    folder_name = now.strftime(f"startrails_%Y%m%d_%H%M_{args.location}")
    output_dir = os.path.join("output", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n📂 Zdjęcia będą zapisywane do: {output_dir}")

    exposure_str = f"{args.exposure:.4f}s".replace(".", ",")  # np. "5,0000s"

    for i in range(1, total_images + 1):
        current_time = datetime.now(tz)
        print(f"[{i}/{total_images}] {current_time.strftime('%H:%M:%S')} | EXP: {args.exposure}s | ISO: {args.iso}")

        subprocess.run(["gphoto2", "--set-config", f"iso={args.iso}"], check=False)
        subprocess.run(["gphoto2", "--set-config", f"shutterspeed={exposure_str}"], check=False)

        filename_base = os.path.join(output_dir, f"IMG_{i:04d}")
        subprocess.run([
            "gphoto2",
            "--capture-image-and-download",
            "--force-overwrite",
            "--filename", f"{filename_base}.%C"
        ], check=False)

        if i % 10 == 0:
            check_battery_level()

        time.sleep(args.gap)

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", choices=["teresin", "tivoli"], default="teresin")
    parser.add_argument("--rule", type=int, choices=[500, 600], default=600)
    parser.add_argument("--focal", type=int, default=35)
    parser.add_argument("--gradient", action="store_true")
    parser.add_argument("--output", type=str)
    parser.add_argument("--simulation", action="store_true")
    parser.add_argument("--altitude", type=float)
    parser.add_argument("--mode", choices=["timelapse", "startrails"])
    parser.add_argument("--duration", type=float)
    parser.add_argument("--interval", type=int, default=1)
    parser.add_argument("--exposure", type=float)
    parser.add_argument("--gap", type=float)
    parser.add_argument("--iso", type=int)

    args = parser.parse_args()

    print_max_exposures()

    if args.simulation:
        if args.altitude is None:
            print("❌ Musisz podać --altitude razem z --simulation")
            exit(1)
        shutter, iso = get_exposure_for_altitude(
            args.altitude, args.focal, args.rule, args.location, apply_gradient=args.gradient
        )
        print(f"\n📍 Lokalizacja: {args.location}")
        print(f"☀️ Wysokość Słońca: {args.altitude:.2f}°")
        print(f"📷 Ogniskowa: {args.focal}mm | Reguła: {args.rule}")
        print(f"🎚 Gradient dnia: {'ON' if args.gradient else 'OFF'}")
        print(f"→ Czas migawki: {shutter:.4f}s")
        print(f"→ ISO: {iso}")
        exit(0)

    if args.mode == "timelapse":
        if args.duration is None:
            print("❌ Wymagany argument --duration dla trybu timelapse")
            exit(1)
        run_timelapse(args)

    if args.mode == "startrails":
        run_startrails(args)

