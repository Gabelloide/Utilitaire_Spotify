import socket
from tkinter.filedialog import FileDialog
from View.ZipUploadPage import ZipUploadPage
from PyQt6.QtWidgets import QFileDialog, QMessageBox

import constants

class ControllerZipUpload:
  def __init__(self, view: ZipUploadPage):
    self.view = view
    self.view.btnZipUpload.clicked.connect(lambda: self.open_file_dialog())


  def open_file_dialog(self):
    fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
    if not fileName.endswith('.zip'):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Error")
        msg.setInformativeText('Please select a zip file')
        msg.setWindowTitle("Error")
        msg.exec()
    else:
        self.send_file(constants.SERVER_ADDRESS, constants.SERVER_ZIP_PORT, fileName)
  
  def send_file(self, server_address, server_port, file_name):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_address, server_port))
            with open(file_name, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    s.sendall(data)
            print(f"File {file_name} sent")
    except socket.error as e:
        print(f"Socket error: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Unexpected error: {e}")