# 📷 Timelapser — Automated Night Photography, Timelapse & Startrails Script

**Timelapser** is a Python tool for automating **timelapse** and **startrails** photography, dynamically adjusting exposure settings based on the Sun's altitude. It uses `gphoto2` to control a DSLR or mirrorless camera and also supports simulation mode for planning shots.

## 🔧 Requirements

- Python 3.7+
- A camera supported by `gphoto2`
- Python packages:
  - `astral`
  - `pytz`

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Timelapse mode — capture images at regular intervals
```bash
python3 exposure_test.py --mode timelapse --duration 2 --interval 300 --location teresin
```

**Parameters:**
- `--duration` — duration in hours
- `--interval` — interval (in seconds) between the start of each photo
- `--location` — predefined location (`teresin` or `tivoli`)
- `--focal` — focal length in mm (default: 35mm)
- `--rule` — rule of 500 or 600 to calculate max night exposure
- `--gradient` — (optional) enables gradual exposure transition between day and night

---

### Startrails mode — long exposures in sequence
```bash
python3 exposure_test.py --mode startrails --duration 1 --exposure 30 --gap 5 --iso 800 --location teresin
```

**Parameters:**
- `--exposure` — exposure time in seconds
- `--gap` — gap between shots in seconds
- `--iso` — fixed ISO setting
- `--duration` — duration in hours

---

### Simulation mode — test exposure without taking photos
```bash
python3 exposure_test.py --simulation --altitude -5 --focal 35 --location teresin --rule 600
```

Displays suggested shutter speed and ISO for a given Sun altitude.

---

## 📂 Output

Photos are saved in the directory: `output/YYYYMMDD_HHMM_<location>/` with the following format:

```
IMG_0001.jpg
IMG_0001.nef
...
```

---

## 🔋 Extra Features

- Battery level check with warning under 15%
- Support for RAW + JPG downloads
- Automatic exposure adjustment based on sunlight elevation

---

## 📈 Roadmap / Ideas

- Support for custom GPS locations or config files
- Precise scheduling based on sunrise/sunset
- GUI or web-based configuration panel
- Cloud backup or file syncing support

---

## 🧑‍💻 Author

Project created by [daniel84k](https://github.com/daniel84k), astrophotography enthusiast.

---

## 📝 License

MIT License
