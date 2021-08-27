from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, \
     QLabel
from PyQt5.QtGui import QFont
from uic import Ui_MainWindow

import GPUtil

import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def labelTebal(teks: str):
        lbl = QLabel(teks)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        lbl.setFont(font)
        return lbl

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.displaySystem()

    def connectSignalsSlots(self):
    ##        self.action_Exit.triggered.connect(self.close)
    ##        self.action_Find_Replace.triggered.connect(self.findAndReplace)
        self.actionAbout.triggered.connect(self.about) #triger untuk menu
        self.btnSystem.clicked.connect(self.displaySystem)
        self.btnCPU.clicked.connect(self.displayCPU) #click untuk buton
        self.btnMemory.clicked.connect(self.displayMemory)
        self.btnDisk.clicked.connect(self.displayDisk)
        self.btnJaringan.clicked.connect(self.displayNet)
        self.btnGPU.clicked.connect(self.displayGPU) #click untuk buton
    def about(self):
        print("diklik")
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )
    def hapusSemuaItem(self):
        while(self.formLayout.rowCount() > 2):
            self.formLayout.removeRow(1)
    def cobaGantiIsi(self):
        self.hapusSemuaItem()
        self.formLayout.insertRow(1, labelTebal("judul"), QLabel("te"))
    def displaySystem(self):
        self.hapusSemuaItem()
        uname = platform.uname()
        head = labelTebal("System")
        tmp = f"{uname.system} {uname.release}"
        self.formLayout.insertRow(1, head, QLabel(tmp))
        head = labelTebal("Version")
        self.formLayout.insertRow(2, head, QLabel(uname.version))
        head = labelTebal("Node Name")
        self.formLayout.insertRow(3, head, QLabel(uname.node))
        head = labelTebal("Machine")
        self.formLayout.insertRow(4, head, QLabel(uname.machine))
        head = labelTebal("Processor")
        self.formLayout.insertRow(5, head, QLabel(uname.processor))

        # Boot Time
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        head = labelTebal("Boot Time")
        self.formLayout.insertRow(5, head, QLabel(f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"))
    def displayCPU(self):
        self.hapusSemuaItem()
        
        # number of cores
        head = labelTebal("Physical cores")
        self.formLayout.insertRow(1, head, QLabel(f"{psutil.cpu_count(logical=False)}"))
        head = labelTebal("Total cores")
        self.formLayout.insertRow(2, head, QLabel(f"{psutil.cpu_count(logical=True)}"))

        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        head = labelTebal("Max Frequency")
        self.formLayout.insertRow(3, head, QLabel(f"{cpufreq.max:.2f}Mhz"))
        head = labelTebal("Min Frequency")
        self.formLayout.insertRow(4, head, QLabel(f"{cpufreq.min:.2f}Mhz"))
        head = labelTebal("Current Frequency")
        self.formLayout.insertRow(5, head, QLabel(f"{cpufreq.current:.2f}Mhz"))

        # CPU usage
        head = labelTebal("CPU Usage Per Core:")
        self.formLayout.insertRow(6, head, QLabel(""))
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            head = labelTebal(f"Core {i}")
            self.formLayout.insertRow(7+i, head, QLabel(f"{percentage}%"))
        head = labelTebal("Total CPU Usage")
        self.formLayout.insertRow(8+i, head, QLabel(f"{psutil.cpu_percent()}%"))
    def displayMemory(self):
        self.hapusSemuaItem()
        # Memory Information
        
        # get the memory details
        svmem = psutil.virtual_memory()
        self.formLayout.insertRow(1, labelTebal("Total"), QLabel(f"{get_size(svmem.total)}"))
        self.formLayout.insertRow(2, labelTebal("Available"), QLabel(f"{get_size(svmem.available)}"))
        self.formLayout.insertRow(3, labelTebal("Used"), QLabel(f"{get_size(svmem.used)}"))
        self.formLayout.insertRow(4, labelTebal("Percentage"), QLabel(f"{svmem.percent}%"))

        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        self.formLayout.insertRow(5, labelTebal("Total"), QLabel(f"{get_size(swap.total)}"))
        self.formLayout.insertRow(6, labelTebal("Free"), QLabel(f"{get_size(swap.free)}"))
        self.formLayout.insertRow(7, labelTebal("Used"), QLabel(f"{get_size(swap.used)}"))
        self.formLayout.insertRow(8, labelTebal("Percentage"), QLabel(f"{swap.percent}%"))
        
    def displayDisk(self):
        self.hapusSemuaItem()
        
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        self.formLayout.insertRow(1, labelTebal("Total read"), QLabel(f"{get_size(disk_io.read_bytes)}"))
        self.formLayout.insertRow(2, labelTebal("Total write"), QLabel(f"{get_size(disk_io.write_bytes)}"))
        
        # Disk Information
        self.formLayout.insertRow(3, labelTebal("Partitions and Usage"), QLabel(f""))
        # get all disk partitions
        rowCounter = 4
        partitions = psutil.disk_partitions()
        for partition in partitions:
            self.formLayout.insertRow(rowCounter, labelTebal(f"Device: {partition.device}"), QLabel(f""))
            self.formLayout.insertRow(rowCounter+1, labelTebal("Mountpoint"), QLabel(f"{partition.mountpoint}"))
            self.formLayout.insertRow(rowCounter+2, labelTebal("File System Type"), QLabel(f"{partition.fstype}"))
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                rowCounter = rowCounter+3
                continue
            self.formLayout.insertRow(rowCounter+3, labelTebal("Total Size"), QLabel(f"{get_size(partition_usage.total)}"))
            self.formLayout.insertRow(rowCounter+4, labelTebal("Used"), QLabel(f"{get_size(partition_usage.used)}"))
            self.formLayout.insertRow(rowCounter+5, labelTebal("Free"), QLabel(f"{get_size(partition_usage.free)}"))
            self.formLayout.insertRow(rowCounter+6, labelTebal("Percentage"), QLabel(f"{partition_usage.percent}%"))
            rowCounter = rowCounter+7
    def displayNet(self):
        self.hapusSemuaItem()
        # Network information
        
        # get all network interfaces (virtual and physical)
        rowCounter = 1
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                self.formLayout.insertRow(rowCounter, labelTebal("Interface"), QLabel(f"{interface_name}"))
                if str(address.family) == 'AddressFamily.AF_INET':
                    self.formLayout.insertRow(rowCounter+1, labelTebal("IP Address"), QLabel(f"{address.address}"))
                    self.formLayout.insertRow(rowCounter+2, labelTebal("Netmask"), QLabel(f"{address.netmask}"))
                    self.formLayout.insertRow(rowCounter+3, labelTebal("Broadcast IP"), QLabel(f"{address.broadcast}"))
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    self.formLayout.insertRow(rowCounter+1, labelTebal("MAC Address"), QLabel(f"{address.address}"))
                    self.formLayout.insertRow(rowCounter+2, labelTebal("Netmask"), QLabel(f"{address.netmask}"))
                    self.formLayout.insertRow(rowCounter+3, labelTebal("Broadcast MAC"), QLabel(f"{address.broadcast}"))
                rowCounter = rowCounter+4
        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        self.formLayout.insertRow(rowCounter, labelTebal("Total Bytes Sent"), QLabel(f"{get_size(net_io.bytes_sent)}"))
        self.formLayout.insertRow(rowCounter+1, labelTebal("Total Bytes Received"), QLabel(f"{get_size(net_io.bytes_recv)}"))
    def displayGPU(self):
        pass

#dialog setting
from PyQt5.uic import loadUi
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)
    
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
