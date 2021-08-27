from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, \
     QLabel
from PyQt5.QtGui import QFont
from uic import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.actionSettings.triggered.connect(self.about)  #fungsinya belum dibikin
        self.actionAbout.triggered.connect(self.about) 
    def about(self):
        QMessageBox.about(
            self,
            "About",
            "<p>Aplikasi untuk mengecek hardware danspesifikasi laptop</p>"
            "<p>- Juga bakal ada alert, mungkin.</p>"
        )
    
def except_hook(cls, exception, traceback):
    "ini untuk debug traceback"
    sys.__excepthook__(cls, exception, traceback)
    
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook #debug dipanggil di sini
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
