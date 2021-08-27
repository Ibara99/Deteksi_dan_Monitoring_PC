from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from uic import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.actionAbout.triggered.connect(self.about) #triger untuk menu
        #self.pushButton.clicked.connect(self.about) #click untuk buton
        
    def about(self):
        QMessageBox.about(
            self,
            "About",
            "<p>Aplikasi untuk mengecek hardware danspesifikasi laptop</p>"
            "<p>- Juga bakal ada alert, mungkin.</p>"
        )

#dialog setting
from PyQt5.uic import loadUi
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
