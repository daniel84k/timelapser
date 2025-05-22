# 📸 Timelapser

**Timelapser** is a Python tool for automatically capturing **timelapse** or **startrails** photos with dynamic settings based on the position of the Sun and user preferences.

## 🚀 Features

- Automatically calculates exposure settings based on astronomical data
- Two modes of operation:
  - `timelapse` – captures photos at regular intervals with dynamic exposure
  - `startrails` – captures long-exposure photos with user-defined parameters
- Simulation mode (logs parameters to CSV without capturing photos)
- Supports multiple shooting locations and file formats
- Customizable lens focal lengths and apertures
- 500/600 rule support for star trail prevention

## 🛠️ Requirements

- Python 3.8+
- Virtualenv (recommended)
- Python dependencies (see `requirements.txt`)
- **gphoto2** – for camera control

### 📷 Installing `gphoto2`

#### macOS (Homebrew):

```bash
brew install gphoto2
```

#### Linux (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install gphoto2
```

#### Windows:

`gphoto2` does not work natively on Windows. To use this application:

- Set up **Windows Subsystem for Linux (WSL)** with Ubuntu:
  - [Official WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- Then install `gphoto2` in WSL:

```bash
sudo apt update
sudo apt install gphoto2
```

### 📦 Installing Python dependencies

After activating your virtual environment:

```bash
pip install -r requirements.txt
```

## 🧪 Example Usage

```bash
python3 main.py --start-time 20:30 --duration 2 --mode timelapse --interval 5 --location location1
```

Startrails mode:

```bash
python3 main.py --mode startrails --exposure 30 --gap 5 --iso 800 --focal 35 --aperture 2.8
```

Simulation mode:

```bash
python3 main.py --simulation --duration 1
```

## ⚙️ Arguments

| Argument         | Description |
|------------------|-------------|
| `--start-time`   | Session start time (e.g. `22:00`) |
| `--duration`     | Duration of the session in hours |
| `--mode`         | `timelapse` or `startrails` |
| `--simulation`   | Run in simulation mode (no photos taken) |
| `--interval`     | Interval between photos (timelapse mode) |
| `--exposure`     | Exposure time in seconds (startrails mode) |
| `--gap`          | Gap between shots in seconds (startrails mode) |
| `--iso`          | ISO setting |
| `--focal`        | Focal length in mm (e.g. 35) |
| `--aperture`     | Aperture value (e.g. 2.8) |
| `--rule`         | Star trail rule: 500 or 600 |
| `--location`     | Shooting location (`location1` or `location2`) |
| `--format`       | File format: `raw`, `jpg`, or `raw+jpg` |
| `--output`       | Output folder for photos |

## 📝 Example Output

```
Max shutter times for each lens with rule 600
 - 14mm: 42.86 s
 - 15mm: 40.00 s
 - 17mm: 35.29 s
...
```

## 🔧 TODO

- GUI interface
- Support for additional locations and languages
- Visualization of exposure schedule

## 📄 License

MIT License – feel free to use, modify, and share!

