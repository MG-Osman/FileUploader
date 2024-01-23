import sys
import subprocess
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QStyle
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QEvent

def upload_to_catbox(file_path):
    """Uploads a file to Catbox and returns the URL."""
    data = {'reqtype': 'fileupload'}
    files = {'fileToUpload': open(file_path, 'rb')}

    try:
        response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
        upload_url = response.text.strip()
        files['fileToUpload'].close()  # Make sure to close the file after uploading

        if response.status_code == 200:
            return f'Upload successful. URL: {upload_url}'
        else:
            return f'Upload failed. Status Code: {response.status_code}'
    except Exception as e:
        return f'An error occurred: {e}'

def download_and_upload(url, log_callback):
    # Get the filename for the best quality video with audio
    result = subprocess.run(['yt-dlp', '--get-filename', '-f', 'best', '-o', '%(title)s.%(ext)s', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        log_callback(f"Failed to get filename for {url}: {result.stderr}")
        return
    file_name = result.stdout.strip()

    # Download the video
    download_result = subprocess.run(['yt-dlp', '-f', 'best', '-o', file_name, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if download_result.returncode != 0:
        log_callback(f"Failed to download {url}: {download_result.stderr}")
        return

    # Upload the file to catbox
    upload_result = upload_to_catbox(file_name)
    log_callback(upload_result)

    # Remove the file after uploading
    try:
        os.remove(file_name)
    except OSError as e:
        log_callback(f"Error removing file {file_name}: {e}")

class CyberpunkButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.default_style = """
            QPushButton {
                color: #39FF14;
                background-color: #000000;
                border: 2px solid #39FF14;
                padding: 5px;
                font: bold 'Consolas';
                font-size: 10pt;
            }
            """
        self.hover_style = """
            QPushButton:hover {
                color: #000000;
                background-color: #39FF14;
                border: 4px solid #39FF14;
                padding: 5px;
            }
            """
        self.setStyleSheet(self.default_style + self.hover_style)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        cyberpunk_font = QFont("Consolas", 10, QFont.Bold)
        neon_green = QColor("#39FF14")
        black_color = QColor("#000000")

        layout = QVBoxLayout()

        self.url_text_edit = QTextEdit()
        self.url_text_edit.setPlaceholderText("Paste URLs here, one per line...")
        self.url_text_edit.setFont(cyberpunk_font)
        self.url_text_edit.setStyleSheet(f"QTextEdit {{"
                                         f"color: {neon_green.name()};"
                                         f"background-color: {black_color.name()};"
                                         f"border: 1px solid {neon_green.name()};"
                                         f"}}")
        layout.addWidget(self.url_text_edit)

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(cyberpunk_font)
        self.log_text_edit.setStyleSheet(f"QTextEdit {{"
                                         f"color: {neon_green.name()};"
                                         f"background-color: {black_color.name()};"
                                         f"border: 1px solid {neon_green.name()};"
                                         f"}}")
        layout.addWidget(self.log_text_edit)

        self.process_button = CyberpunkButton('Process URLs')
        self.process_button.clicked.connect(self.process_urls)
        layout.addWidget(self.process_button)

        self.upload_button = CyberpunkButton('Upload Local File')
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.setLayout(layout)
        self.setWindowTitle('MG-FileUploader')
        self.setGeometry(300, 300, 600, 400)

        palette = self.palette()
        palette.setColor(QPalette.Window, black_color)
        palette.setColor(QPalette.WindowText, neon_green)
        self.setPalette(palette)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].scheme() == 'file':
            dropped_file_path = str(urls[0].path())[1:]  # Extract path and strip leading '/'
            self.log(f'Uploading dragged file: {dropped_file_path}')
            upload_result = upload_to_catbox(dropped_file_path)
            self.log(upload_result)

    def log(self, message):
        self.log_text_edit.append(message)

    def process_urls(self):
        urls = self.url_text_edit.toPlainText().split('\n')
        for url in urls:
            if url.strip():
                self.log(f'Processing URL: {url.strip()}')
                download_and_upload(url.strip(), self.log)

    def upload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload", "", "All Files (*);;", options=options)
        if file_path:
            self.log(f'Uploading local file: {file_path}')
            upload_result = upload_to_catbox(file_path)
            self.log(upload_result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
