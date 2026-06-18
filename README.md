## StreamFetch
A graphical shell using the yt-dlp library. Built with Python and PySide6.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-6.11+-41CD52?logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey" alt="Platform">
</p>

---
## Windows Installation

> For Windows users, a pre-built `.exe` is available — no Python required.

| Platform | Download |
|----------|----------|
| Windows | [![Download](https://img.shields.io/badge/Download-.exe-blue?logo=windows)](https://github.com/r3cruit1337/streamfetch/releases/latest) |

## Overview

`Stream Fetch` is an app that leverages the `yt-dlp` library to download media from supported stream sources.
It provides:

- URL input for supported stream links
- format selection for video and audio output
- progress display and cancellation support
- selectable output folder
- inline log output for download status

---

## Requirements

- Python 3.12+
- `PySide6`
- `yt-dlp`
- `imageio-ffmpeg`

Dependencies are listed in `requirements.txt`.

---

## Linux installation

1. Clone this repository:

```bash
# Activate virtual environment (bash/zsh)
git clone https://github.com/r3cruit1337/streamfetch.git
cd streamfetch
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the app

Start the GUI from the repository root:

```bash
python src/main.py
```

The default output folder on Linux is `~/Downloads`.

---

## Usage

1. Paste a supported stream URL into the `Video URL` field.
2. Choose a download format from the dropdown.
3. Select an output folder if needed.
4. Click `DOWNLOAD`.
5. Use `CANCEL` to stop the current download.
6. Click `Open Folder` after the download completes.

---

## Supported Options

Preconfigured download formats include:

- Best quality video + audio
- 1080p MP4
- 720p MP4
- 480p MP4
- Audio only (MP3)
- Audio only (best available)

---

## Notes

- This app is a GUI wrapper around the `yt-dlp` library.
- Downloads are saved to the selected output folder.
- Playlist downloads are supported and progress is updated per item.

---

## License

[MIT License](LICENSE).

