from shutter_utils import set_closest_shutter_speed
from iso_utils import set_closest_iso

def set_camera_settings(shutter, iso, focal_length, rule):
    max_shutter = rule / focal_length
    set_closest_shutter_speed(shutter, max_shutter)
    set_closest_iso(iso, max_iso=1600)

