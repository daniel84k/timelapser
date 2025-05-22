import os
import time
import datetime
import subprocess
from utils import format_shutter_value

def capture_image(shutter, iso, focal, aperture, location, image_format, index=None, exposure_mode="timelapse"):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    image_number = f"{index:04d}" if index is not None else "0000"
    mode = "startrails" if exposure_mode == "startrails" else "timelapse"

    # Formatowane parametry
    shutter_str = format_shutter_value(shutter).replace("/", "_").replace(".", "_")
    iso_str = f"ISO{iso}"
    focal_str = f"F{focal}"

    # Nowy schemat: <tryb>_<data>_<czas>_F<focal>_ISO<iso>_S<shutter>_<numer>
    base_filename = f"{mode}_{date_str}_{time_str}_{focal_str}_{iso_str}_S{shutter_str}_{image_number}"

    print(f"Robienie zdjęcia: {base_filename}")

    files_before = set(os.listdir("."))
    subprocess.run(["gphoto2", "--capture-image-and-download"], check=False)
    time.sleep(1)
    files_after = set(os.listdir("."))
    new_files = files_after - files_before

    for fname in new_files:
        lower = fname.lower()
        if lower.endswith(".nef"):
            target = f"{base_filename}.NEF"
            if not os.path.exists(target):
                os.rename(fname, target)
                print(f"Zapisano: {target}")
        elif lower.endswith(".jpg"):
            size = os.path.getsize(fname)
            if size == 0:
                print(f"Usuwanie pustego JPG: {fname}")
                os.remove(fname)
            else:
                target = f"{base_filename}.JPG"
                if not os.path.exists(target):
                    os.rename(fname, target)
                    print(f"Zapisano: {target}")

