import sys
import subprocess
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class UploadThread(QThread):
    log = pyqtSignal(str)
    completed = pyqtSignal()

    def __init__(self, file_path, parent=None):
        super(UploadThread, self).__init__(parent)
        self.file_path = file_path

    def run(self):
        self.upload_to_catbox(self.file_path)

    def upload_to_catbox(self, file_path):
        """Uploads a file to Catbox and returns the URL."""
        data = {'reqtype': 'fileupload'}
        files = {'fileToUpload': open(file_path, 'rb')}

        try:
            response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
            upload_url = response.text.strip()
            files['fileToUpload'].close()  # Make sure to close the file after uploading

            if response.status_code == 200:
                self.log.emit(f'Upload successful. URL: {upload_url}')
            else:
                self.log.emit(f'Upload failed. Status Code: {response.status_code}')
        except Exception as e:
            self.log.emit(f'An error occurred: {e}')
        finally:
            self.completed.emit()

class DownloadUploadThread(QThread):
    log = pyqtSignal(str)
    completed = pyqtSignal()

    def __init__(self, url, parent=None):
        super(DownloadUploadThread, self).__init__(parent)
        self.url = url

    def run(self):
        self.download_and_upload(self.url)

    def download_and_upload(self, url):
        # Get the filename for the best quality video with audio
        result = subprocess.run(['yt-dlp', '--get-filename', '-f', 'best', '-o', '%(title)s.%(ext)s', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            self.log.emit(f"Failed to get filename for {url}: {result.stderr}")
            self.completed.emit()
            return
        file_name = result.stdout.strip()

        # Download the video
        download_result = subprocess.run(['yt-dlp', '-f', 'best', '-o', file_name, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if download_result.returncode != 0:
            self.log.emit(f"Failed to download {url}: {download_result.stderr}")
            self.completed.emit()
            return

        # Upload the file to catbox
        self.upload_to_catbox(file_name)

        # Remove the file after uploading
        try:
            os.remove(file_name)
        except OSError as e:
            self.log.emit(f"Error removing file {file_name}: {e}")

    def upload_to_catbox(self, file_path):
        """Uploads a file to Catbox and returns the URL."""
        data = {'reqtype': 'fileupload'}
        files = {'fileToUpload': open(file_path, 'rb')}

        try:
            response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
            upload_url = response.text.strip()
            files['fileToUpload'].close()  # Make sure to close the file after uploading

            if response.status_code == 200:
                self.log.emit(f'Upload successful. URL: {upload_url}')
            else:
                self.log.emit(f'Upload failed. Status Code: {response.status_code}')
        except Exception as e:
            self.log.emit(f'An error occurred: {e}')
        finally:
            self.completed.emit()

class CyberpunkButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                color: #39FF14;
                background-color: #1a1a1a;
                border: 2px solid #39FF14;
                border-radius: 15px;
                padding: 10px;
                font: bold 12pt 'Consolas';
            }
            QPushButton:hover {
                color: #1a1a1a;
                background-color: #39FF14;
            }
            QPushButton:pressed {
                background-color: #2eb811;
            }
        """)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        cyberpunk_font = QFont("Consolas", 10, QFont.Bold)
        neon_green = QColor("#39FF14")
        dark_gray = QColor("#1a1a1a")

        layout = QVBoxLayout()
        layout.setSpacing(15)

        header = QLabel("MG-FileUploader")
        header.setFont(QFont("Consolas", 24, QFont.Bold))
        header.setStyleSheet(f"color: {neon_green.name()}; margin-bottom: 10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        self.url_text_edit = QTextEdit()
        self.url_text_edit.setPlaceholderText("Paste URLs here, one per line...")
        self.url_text_edit.setFont(cyberpunk_font)
        self.url_text_edit.setStyleSheet(f"""
            QTextEdit {{
                color: {neon_green.name()};
                background-color: {dark_gray.name()};
                border: 2px solid {neon_green.name()};
                border-radius: 15px;
                padding: 10px;
            }}
        """)
        layout.addWidget(self.url_text_edit)

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(cyberpunk_font)
        self.log_text_edit.setStyleSheet(f"""
            QTextEdit {{
                color: {neon_green.name()};
                background-color: {dark_gray.name()};
                border: 2px solid {neon_green.name()};
                border-radius: 15px;
                padding: 10px;
            }}
        """)
        layout.addWidget(self.log_text_edit)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                color: {neon_green.name()};
                background-color: {dark_gray.name()};
                border: 2px solid {neon_green.name()};
                border-radius: 10px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {neon_green.name()};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(self.progress_bar)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.process_button = CyberpunkButton('Process URLs')
        self.process_button.clicked.connect(self.process_urls)
        buttons_layout.addWidget(self.process_button)

        self.upload_button = CyberpunkButton('Upload Local File')
        self.upload_button.clicked.connect(self.upload_file)
        buttons_layout.addWidget(self.upload_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.setWindowTitle('MG-FileUploader')
        self.setGeometry(300, 300, 700, 500)

        palette = self.palette()
        palette.setColor(QPalette.Window, dark_gray)
        palette.setColor(QPalette.WindowText, neon_green)
        self.setPalette(palette)

        self.setWindowIcon(QIcon('icon.png'))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].scheme() == 'file':
            dropped_file_path = str(urls[0].toLocalFile())
            self.log(f'Uploading dragged file: {dropped_file_path}')
            self.start_upload(dropped_file_path)

    def log(self, message):
        self.log_text_edit.append(message)

    def reset_progress_bar(self):
        self.progress_bar.reset()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Please wait...")
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                color: #39FF14;
                background-color: #1a1a1a;
                border: 2px solid #39FF14;
                border-radius: 10px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: #39FF14;
                border-radius: 8px;
            }}
        """)

    def start_upload(self, file_path):
        self.reset_progress_bar()
        self.upload_thread = UploadThread(file_path)
        self.upload_thread.log.connect(self.log)
        self.upload_thread.completed.connect(self.upload_completed)
        self.upload_thread.start()

    def start_download_upload(self, url):
        self.reset_progress_bar()
        self.download_upload_thread = DownloadUploadThread(url)
        self.download_upload_thread.log.connect(self.log)
        self.download_upload_thread.completed.connect(self.upload_completed)
        self.download_upload_thread.start()

    def upload_completed(self):
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("Completed!")
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                color: black;
                background-color: #1a1a1a;
                border: 2px solid #39FF14;
                border-radius: 10px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: #39FF14;
                border-radius: 8px;
            }}
        """)

    def process_urls(self):
        urls = self.url_text_edit.toPlainText().split('\n')
        for url in urls:
            if url.strip():
                self.log(f'Processing URL: {url.strip()}')
                self.start_download_upload(url.strip())

    def upload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload", "", "All Files (*);;", options=options)
        if file_path:
            self.log(f'Uploading local file: {file_path}')
            self.start_upload(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
