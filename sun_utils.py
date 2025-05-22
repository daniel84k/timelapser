from astral.sun import sun, elevation
from astral.location import Observer
import datetime
from pytz import timezone

def calculate_sun_altitude(lat, lon, tz):
    now = datetime.datetime.now(datetime.timezone.utc)
    observer = Observer(latitude=lat, longitude=lon)
    alt = elevation(observer=observer, dateandtime=now)
    s = sun(observer=observer, date=now, tzinfo=timezone(tz))
    return alt, s['sunrise'], s['sunset']

