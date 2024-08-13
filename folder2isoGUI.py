#!/bin/python3

from PyQt5.QtWidgets import (
    QFileDialog,
    QLabel,
    QSizePolicy,
    QWidget,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QMessageBox,
    QLineEdit,
)

from PyQt5.QtGui import QFont

import os
import sys

from folder2iso import *


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        title = os.path.basename(sys.argv[0]).replace(".py", "")
        self.setWindowTitle(f"{title} {FOLDER2ISO_VERSION}")
        self.resize(250, 180)
        self.setAcceptDrops(True)

        self.prefix = "<datetime format here>"

        widget = QWidget()
        layout = QVBoxLayout()
        self.display = QLabel("Drag folder here", widget)
        self.display.setFont(QFont("Arial", 25))
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.display)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if not os.path.isfile(f):
                iso = self.saveFileDialog()
                if iso != None:
                    if not iso.lower().endswith(".iso"):
                        iso += ".iso"
                    if create_iso_from_folder(f, iso) == 0:
                        QMessageBox.information(self, "Success!", f"Created {iso}")
                    else:
                        QMessageBox.critical(self, "Error!", f"Failed to create {iso}")

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save ISO file", "", "ISO Files (*.iso)", options=options
        )
        if fileName:
            return fileName
            print(fileName)
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())
