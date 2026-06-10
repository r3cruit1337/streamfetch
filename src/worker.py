import os
import re
import sys
import yt_dlp
import imageio_ffmpeg

from PySide6.QtCore import (
    QObject, Signal, Slot
)

#YT-DLP Logger
class YtdlpLogger:
    def __init__(self, worker: "DownloadWorker"):
        self._worker = worker
    def debug(self, msg: str) -> None:
        if msg.startswith("[debug]"):
            return
        self._worker.log_message.emit("info", msg)

    def info(self, msg: str) -> None:
        self._worker.log_message.emit("info", msg)

    def warning(self, msg: str) -> None:
        self._worker.log_message.emit("warning", msg)

    def error(self, msg: str) -> None:
        self._worker.log_message.emit("error", msg)

#Download worker
class DownloadWorker(QObject):
    log_message = Signal(str, str)
    progress_update = Signal(int)
    download_finished = Signal(bool)
    playlist_update = Signal(int, int)

    def __init__(self, url:str, output_dir: str, format_code: str):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.format_code = format_code
        self._logger = YtdlpLogger(self)
        self._cancelled = False

    def _progress_hook(self, d:dict) -> None:
        if self._cancelled:
            raise yt_dlp.utils.DownloadError("Download cancelled by user")
        status = d.get("status")
        playlist_index = d.get("playlist_index")
        playlist_total = d.get("playlist_count")
        if playlist_index and playlist_total:
            self.playlist_update.emit(int(playlist_index), int(playlist_total))
        
        if status == "downloading":
            percent_raw = d.get("_percent_str", "0%").strip()
            percent_num = re.sub(r"[^\d.]", "", percent_raw)
            try:
                percent = int(float(percent_num))
            except ValueError:
                percent = 0
            self.progress_update.emit(min(percent, 99))

            speed = d.get("_speed_str", "N/A").strip()
            eta = d.get("_eta_str", "N/A").strip()
            total = d.get("_total_bytes_str", d.get("_total_bytes_estimate_str", "?")).strip()
            self.log_message.emit("info", f" Downloading ... {percent_raw:>6} | speed {speed} | ETA {eta} | size {total}")
        elif status == "finished":
            self.progress_update.emit(100)
            filename = os.path.basename(d.get("filename", ""))
            self.log_message.emit("success", f" ✔  Download complete → {filename}")
        elif status == "error":
            self.log_message.emit("error", f"✘  yt-dlp reported an error during download")
    def cancel(self) -> None:
        self._cancelled = True
    
    @Slot()
    def run(self) -> None:
        self.log_message.emit("info", f"▶  Starting download")
        self.log_message.emit("info", f"   URL    : {self.url}")
        self.log_message.emit("info", f"   Folder : {self.output_dir}")
        self.log_message.emit("info", f"   Format : {self.format_code}")
        self.log_message.emit("info", "─" * 60)
        
        if sys.platform == "win32":
            outtmpl = os.path.join(self.output_dir, "%(title).150B.%(ext)s")
        else:
            outtmpl = os.path.join(self.output_dir, "%(title).100B.%(ext)s")

        ydl_opts = {
            "outtmpl": outtmpl,
            "format": self.format_code,
            "logger": self._logger,
            "progress_hooks": [self._progress_hook],
            "merge_output_format": "mp4",
            "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
            "quiet": False,
            "no_warnings": False,
            "retries": 5,
            "fragment_retries": 10,
            "nooverwrites": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.log_message.emit("success", "✔  All done!")
            self.download_finished.emit(True)

        except yt_dlp.utils.DownloadError as exc:
            self.log_message.emit("error", f"✘  Download error: {exc}")
            self.download_finished.emit(False)

        except Exception as exc:
            self.log_message.emit("error", f"✘  Unexpected error: {exc}")
            self.download_finished.emit(False)