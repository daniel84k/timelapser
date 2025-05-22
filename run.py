import os
import time
import datetime
import csv
import logging
from pytz import timezone

from config.locations import locations
from sun_utils import calculate_sun_altitude
from exposure import get_shutter_speed_and_iso
from capture import capture_image
from settings import set_camera_settings
from battery import get_battery_level

logging.basicConfig(filename='timelapse_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

def run_timelapse(args):
    if args.location not in locations:
        raise ValueError("Unsupported location. Use 'tivoli' or 'teresin'")

    lat, lon, tz = locations[args.location]
    now = datetime.datetime.now(timezone(tz))

    # 🔋 Sprawdzenie poziomu baterii na starcie
    get_battery_level()

    if args.start_time:
        hour, minute = map(int, args.start_time.split(":"))
        start_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if start_time < now:
            start_time += datetime.timedelta(days=1)
        wait_time = (start_time - now).total_seconds()
        print(f"Waiting until {start_time.strftime('%H:%M')} ({int(wait_time)}s)...")
        time.sleep(wait_time)
    else:
        start_time = now

    folder_name = start_time.strftime(f"timelapse_%Y%m%d_%H%M%S_{args.location}")
    output_path = os.path.join(args.output, folder_name)
    os.makedirs(output_path, exist_ok=True)
    os.chdir(output_path)

    if args.mode == 'startrails':
        missing = []
        if args.exposure is None: missing.append('--exposure')
        if args.gap is None: missing.append('--gap')
        if args.duration is None: missing.append('--duration')
        if args.iso is None: missing.append('--iso')
        if missing:
            raise ValueError(f"W trybie startrails musisz podać: {', '.join(missing)}")

        # 🔒 Zabezpieczenie przed za długim czasem względem rule/focal
        max_shutter = args.rule / args.focal
        if args.exposure > max_shutter:
            raise ValueError(
                f"❌ Czas ekspozycji {args.exposure}s przekracza maksymalny czas {max_shutter:.2f}s wg reguły {args.rule} i ogniskowej {args.focal}mm."
            )

        end_time = start_time + datetime.timedelta(hours=args.duration)
        total_images = int((end_time - start_time).total_seconds() // (args.exposure + args.gap))

        print(f"[Startrails] Czas ekspozycji: {args.exposure}s, przerwa: {args.gap}s, ISO: {args.iso}")
        print(f"Zrobisz {total_images} zdjęć przez {args.duration} godzin.")

        fps_list = [24, 30]
        for fps in fps_list:
            movie_seconds = total_images / fps
            print(f"  - długość filmu przy {fps}fps: {movie_seconds:.1f} s ({movie_seconds / 60:.1f} min)")

        for i in range(total_images):
            now = datetime.datetime.now(timezone(tz))
            print(f"[{i+1}/{total_images}] Time: {now} Exposure: {args.exposure}s ISO: {args.iso}")
            logging.info(f"Image {i+1}: {now} Exposure: {args.exposure} ISO: {args.iso}")

            # ✅ Ustawienia aparatu z ograniczeniem max_shutter + ISO
            set_camera_settings(args.exposure, args.iso, args.focal, args.rule)

            capture_image(args.exposure, args.iso, args.focal, args.aperture, args.location, args.format, index=i+1, exposure_mode=args.mode)

            if (i + 1) % 10 == 0:
                get_battery_level()

            time.sleep(args.gap)

        print("Startrails complete.")
        logging.info("Startrails complete.")
        return

    # Timelapse mode
    duration = args.duration if args.duration else 24
    end_time = start_time + datetime.timedelta(hours=duration)
    total_images = int((end_time - start_time).total_seconds() // args.interval)

    fps_list = [24, 30]
    print(f"[Timelapse] Zdjęć: {total_images}")
    for fps in fps_list:
        movie_seconds = total_images / fps
        print(f"  - długość filmu przy {fps}fps: {movie_seconds:.1f} s ({movie_seconds / 60:.1f} min)")

    if args.simulation:
        sim_file = f"simulation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(sim_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Image', 'Time', 'Altitude', 'Shutter', 'ISO', 'Focal', 'Aperture'])
            for i in range(total_images):
                sim_time = start_time + datetime.timedelta(seconds=i * args.interval)
                altitude = calculate_sun_altitude(lat, lon, tz)[0]
                shutter, iso = get_shutter_speed_and_iso(altitude, args.focal, args.aperture, args.rule)
                writer.writerow([i + 1, sim_time.isoformat(), round(altitude, 2), round(shutter, 4), iso, args.focal, args.aperture])
        print(f"Simulation complete. Output saved to {sim_file}")
        return

    image_count = 0
    while datetime.datetime.now(timezone(tz)) < end_time:
        try:
            now = datetime.datetime.now(timezone(tz))
            altitude, _, _ = calculate_sun_altitude(lat, lon, tz)
            shutter, iso = get_shutter_speed_and_iso(altitude, args.focal, args.aperture, args.rule)

            print(f"[{image_count + 1}/{total_images}] Time: {now} Altitude: {altitude:.2f}° Shutter: {shutter:.4f}s ISO: {iso}")
            logging.info(f"Image {image_count + 1}: {now} Alt: {altitude:.2f} Shutter: {shutter:.4f} ISO: {iso}")

            set_camera_settings(shutter, iso, args.focal, args.rule)

            capture_image(shutter, iso, args.focal, args.aperture, args.location, args.format, index=image_count+1, exposure_mode=args.mode)

            if (image_count + 1) % 10 == 0:
                get_battery_level()

            image_count += 1
            time.sleep(args.interval)

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")

    print("Timelapse complete.")
    logging.info("Timelapse complete.")

