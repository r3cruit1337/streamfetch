import os
import re
from constants import APP_TITLE, APP_VERSION

from worker import DownloadWorker

from PySide6.QtCore import (
    Qt, QThread, Slot, QUrl
)
from PySide6.QtGui import (
    QDesktopServices
)
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTextEdit, QFileDialog, QComboBox,
    QProgressBar, QFrame, QSizePolicy
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._thread: QThread | None = None
        self._worker: DownloadWorker | None = None
        self._output_dir: str = os.path.expanduser("~/Downloads")
        os.makedirs(self._output_dir, exist_ok=True)
        self._build_ui()
        self._connect_signals()
    
    #Build UI
    def _build_ui(self) -> None:
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(760, 580)
        self.resize(860, 660)
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 15)
        root.setSpacing(14)

        #Header
        header = QHBoxLayout()
        title = QLabel("StreamFetch")
        title.setObjectName("titleLabel")
        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setObjectName("subtitleLabel")
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(version_label)
        root.addLayout(header)
        root.addWidget(self._hline())

        # URL label
        url_label = QLabel("Video URL")
        url_label.setObjectName("sectionLabel")
        root.addWidget(url_label)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=…")
        self.url_input.setClearButtonEnabled(True)
        root.addWidget(self.url_input)

        #Option
        option_label = QLabel("OPTIONS")
        option_label.setObjectName("sectionLabel")
        root.addWidget(option_label)
        option_row = QHBoxLayout()
        option_row.setSpacing(10)
        self.video_format = QComboBox()
        self.video_format.setToolTip("Select download quality / format")
        for label, code in [
            ("Best quality (video+audio)", "bestvideo+bestaudio/best"),
            ("1080p MP4",                  "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"),
            ("720p MP4",                   "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"),
            ("480p MP4",                   "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"),
            ("Audio only (MP3)",           "bestaudio[ext=mp3]/bestaudio"),
            ("Audio only (best)",          "bestaudio/best"),
        ]:
            self.video_format.addItem(label, userData=code)
        option_row.addWidget(self.video_format, stretch=1)
        self.folder_button = QPushButton("📁  Output Folder")
        self.folder_button.setToolTip(f"Current: {self._output_dir}")
        option_row.addWidget(self.folder_button)
        root.addLayout(option_row)

        #Action row
        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress_bar.setFixedHeight(28)
        action_row.addWidget(self.progress_bar, stretch=1)
        
        self.download_button = QPushButton("DOWNLOAD")
        self.download_button.setObjectName("downloadBtn")
        self.download_button.setFixedHeight(40)
        action_row.addWidget(self.download_button)

        self.cancel_button = QPushButton("CANCEL")
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setEnabled(False)
        action_row.addWidget(self.cancel_button)

        root.addLayout(action_row)

        #Footer
        footer_row = QHBoxLayout()
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("subtitleLabel")
        footer_row.addWidget(self.status_label, stretch=1)

        self.open_folder_button = QPushButton("📂  Open Folder")
        self.open_folder_button.setFixedHeight(35)
        self.open_folder_button.setToolTip("Open the output folder in your file manager")
        self.open_folder_button.setEnabled(False)
        footer_row.addWidget(self.open_folder_button)

        root.addLayout(footer_row)

        #Log
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(120)
        self.log_output.setPlaceholderText("Log output...")
        root.addWidget(self.log_output)

        root.addStretch()

    @staticmethod
    def _hline() -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        return line
    
    def _connect_signals(self) -> None:
        self.download_button.clicked.connect(self._on_download_clicked)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        self.folder_button.clicked.connect(self._on_pick_folder)
        self.open_folder_button.clicked.connect(self._on_open_folder)
        self.url_input.returnPressed.connect(self._on_download_clicked)

    @Slot()
    def _on_cancel_clicked(self) -> None:
        if self._worker is not None:
            self._worker.cancel()
            self._log("warning", "⚠  Cancellation requested — stopping after current fragment …")
            self.cancel_button.setEnabled(False)
            self.status_label.setText("Cancelling …")
    
    @Slot()
    def _on_open_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(self._output_dir))
    
    @Slot(int, int)
    def _on_playlist_update(self, current: int, total: int) -> None:
        self.status_label.setText(f"Downloading video {current} of {total} …")
        self.progress_bar.setValue(0)
    
    @Slot()
    def _on_pick_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self._output_dir, QFileDialog.Option.ShowDirsOnly)
        if folder:
            self._output_dir = folder
            self.folder_button.setToolTip(f"Current: {self._output_dir}")
            self._log("info", f"  Output folder changed -> {self._output_dir}")
    
    @Slot()
    def _on_download_clicked(self) -> None:
        if self._thread and self._thread.isRunning():
            return
        url = self.url_input.text().strip()
        if not url:
            self._log("error", "✘  Please enter a YouTube URL first.")
            self.url_input.setFocus()
            return
        if not (url.startswith("http://") or url.startswith("https://")):
            self._log("error", "✘  URL must start with http:// or https://")
            return
        if not os.path.isdir(self._output_dir):
            self._log("error", f"✘  Output folder does not exist: {self._output_dir}")
            return
        format_code = self.video_format.currentData()

        self._thread = QThread(self)
        self._worker = DownloadWorker(url, self._output_dir, format_code)
        self._worker.moveToThread(self._thread)

        self._worker.log_message.connect(self._log)
        self._worker.progress_update.connect(self.progress_bar.setValue)
        self._worker.playlist_update.connect(self._on_playlist_update)
        self._worker.download_finished.connect(self._on_download_finished)

        self._thread.started.connect(self._worker.run)

        self._worker.download_finished.connect(self._thread.quit)
        self._worker.download_finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._set_downloading(True)
        self.progress_bar.setValue(0)

        self._thread.start()
    
    @Slot(bool)
    def _on_download_finished(self, success: bool) -> None:
        self._set_downloading(False)
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("✔  Download finished")
            self.open_folder_button.setEnabled(True)
        else:
            self.status_label.setText("✘  Download failed — see log above")
    
    def _set_downloading(self, active: bool) -> None:
        self.download_button.setDisabled(active)
        self.cancel_button.setEnabled(active)
        self.url_input.setDisabled(active)
        self.video_format.setDisabled(active)
        self.folder_button.setDisabled(active)
        if active:
            self.status_label.setText("Downloading ...")
        else:
            self.status_label.setText("Ready")
    
    @Slot(str, str)
    def _log(self, level: str, message: str) -> None:
        if level in ("success", "error", "warning", "info"):
            clean = re.sub(r'\x1b\[[0-9;]*m', '', message).strip()
            #developer
            print(f"[{level.upper()}] {clean}")
            #user
            if level == "success":
                self.log_output.append(f'<span style="color:#44cc88;">✔ {clean}</span>')
            elif level == "error":
                self.log_output.append(f'<span style="color:#ff5555;">✘ {clean}</span>')
            elif level == "warning":
                self.log_output.append(f'<span style="color:#ffaa44;">⚠ {clean}</span>')
            elif level == "info":
                if "Destination:" in clean:
                    filename = clean.split("Destination:")[-1].strip()
                    self.log_output.append(f'<span style="color:#4488ff;">📄 Saving: {filename}</span>')
                elif clean.startswith("▶"):
                    self.log_output.append('<span style="color:#4488ff;">⟳ Starting download...</span>')