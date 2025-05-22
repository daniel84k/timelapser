import numpy as np

def get_shutter_speed_and_iso(altitude, focal_length, aperture, rule):
    max_shutter = rule / focal_length
    min_shutter = 1 / 4000
    min_iso, max_iso = 100, 1600
    norm_alt = np.clip((altitude + 5) / 60, 0, 1)

    log_shutter = np.log10(min_shutter) + (np.log10(max_shutter) - np.log10(min_shutter)) * (1 - norm_alt)
    raw_shutter = 10 ** log_shutter

    allowed_shutter = [
        1/4000, 1/3200, 1/2500, 1/2000, 1/1600, 1/1250, 1/1000,
        1/800, 1/640, 1/500, 1/400, 1/320, 1/250, 1/200, 1/160,
        1/125, 1/100, 1/80, 1/60, 1/50, 1/40, 1/30, 1/25, 1/20,
        1/15, 1/13, 1/10, 1/8, 1/6, 1/5, 1/4, 1/3, 0.4, 0.5, 0.6,
        0.8, 1, 1.3, 1.6, 2, 2.5, 3.2, 4, 5, 6, 8, 10, 13, max_shutter
    ]
    allowed_shutter = [s for s in allowed_shutter if s <= max_shutter]
    shutter = min(allowed_shutter, key=lambda x: abs(x - raw_shutter))

    log_iso = np.log10(min_iso) + (np.log10(max_iso) - np.log10(min_iso)) * (1 - norm_alt)
    raw_iso = 10 ** log_iso
    allowed_iso = [100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600]
    iso = min(allowed_iso, key=lambda x: abs(x - raw_iso))

    return shutter, iso

