from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QMessageBox, \
     QLabel
from PyQt5.QtGui import QFont
from uic import Ui_MainWindow
import psutil
import platform
from datetime import datetime
import GPUtil

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

class Window(QMainWindow, Ui_MainWindow):   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.actionSettings.triggered.connect(self.about)  #fungsinya belum dibikin
        self.actionAbout.triggered.connect(self.about)
        
        self.systeminfo()
        self.summry()
        self.cpuInfo()
        self.gpuInfo()
        self.mmrInfo()
        self.diskInfo()
        self.jrngInfo()

    def about(self):
        QMessageBox.about(
            self,
            "About",
            "<p>Aplikasi untuk mengecek hardware dan spesifikasi laptop</p>"
            "<p>- Juga bakal ada alert, mungkin.</p>"
        )

    def summry(self):
        uname = platform.uname()
        os = uname.system
        dvname = uname.node
        phycore = str(psutil.cpu_count(logical=False))
        ttlcore = str(psutil.cpu_count(logical=True))
        cpufreq = psutil.cpu_freq()

        self.summaryTab.addItem("Operating Sistem: ")
        self.summaryTab.addItem(os)
        self.summaryTab.addItem(" ")
        self.summaryTab.addItem("Nama Perangkat: ")
        self.summaryTab.addItem(dvname)
        self.summaryTab.addItem(" ")
        self.summaryTab.addItem("=====[ CPU ]=====")
        self.summaryTab.addItem(" ")
        self.summaryTab.addItem("CPU Frequency: ")
        self.summaryTab.addItem(f"{cpufreq.max:.2f}Mhz")
        self.summaryTab.addItem(" ")
        self.summaryTab.addItem("Physical cores: ")
        self.summaryTab.addItem(phycore)
        self.summaryTab.addItem(" ")
        self.summaryTab.addItem("Total cores: ")
        self.summaryTab.addItem(ttlcore)
        self.summaryTab.addItem(" ")
        
    def systeminfo(self):
        uname = platform.uname()
        os = uname.system
        dvname = uname.node
        rls = uname.release
        vrs = uname.version
        mchn = uname.machine
        proc = uname.processor
        
        self.informatiionTab.addItem("Operating Sistem : ")
        self.informatiionTab.addItem(os)
        self.informatiionTab.addItem(" ")
        self.informatiionTab.addItem("Nama Perangkat : ")
        self.informatiionTab.addItem(dvname)
        self.informatiionTab.addItem(" ")
        self.informatiionTab.addItem("Release : ")
        self.informatiionTab.addItem(rls)
        self.informatiionTab.addItem(" ")
        self.informatiionTab.addItem("Version : ")
        self.informatiionTab.addItem(vrs)
        self.informatiionTab.addItem(" ")
        self.informatiionTab.addItem("Machine : ")
        self.informatiionTab.addItem(mchn)
        self.informatiionTab.addItem(" ")
        self.informatiionTab.addItem("Processor : ")
        self.informatiionTab.addItem(proc)

    def cpuInfo(self):
        phycore = str(psutil.cpu_count(logical=False))
        ttlcore = str(psutil.cpu_count(logical=True))

        cpufreq = psutil.cpu_freq()
        
        ttlcpuusg = str(psutil.cpu_percent())

        self.cpuTab.addItem("Physical cores : ")
        self.cpuTab.addItem(phycore)
        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("Total cores : ")
        self.cpuTab.addItem(ttlcore)
        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("Max Frequency : ")
        self.cpuTab.addItem(f"{cpufreq.max:.2f}Mhz")
        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("Min Frequency : ")
        self.cpuTab.addItem(f"{cpufreq.min:.2f}Mhz")
        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("Current Frequency : ")
        self.cpuTab.addItem(f"{cpufreq.current:.2f}Mhz")
        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("CPU Usage Per Core:")

        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            self.cpuTab.addItem(f"Core {i}: {percentage}%")

        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("Total CPU Usage:")
        self.cpuTab.addItem(f"{psutil.cpu_percent()}%")       
        
    def gpuInfo(self):
        pass

    def mmrInfo(self):
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        self.memoryUsageTab.addItem("====[Memory Information]=====")
        self.memoryUsageTab.addItem(f"Total: {get_size(svmem.total)}")
        self.memoryUsageTab.addItem(f"Available: {get_size(svmem.available)}")
        self.memoryUsageTab.addItem(f"Used: {get_size(svmem.used)}")
        self.memoryUsageTab.addItem(f"Percentage: {svmem.percent}%")
        self.memoryUsageTab.addItem("")

        self.memoryUsageTab.addItem("====[SWAP]=====")
        self.memoryUsageTab.addItem(f"Total: {get_size(swap.total)}")
        self.memoryUsageTab.addItem(f"Free: {get_size(swap.free)}")
        self.memoryUsageTab.addItem(f"Used: {get_size(swap.used)}")
        self.memoryUsageTab.addItem(f"Percentage: {swap.percent}%")
    
    def diskInfo(self):
        partitions = psutil.disk_partitions()
        for partition in partitions:
            self.diskUsageTab.addItem(f"=== Device: {partition.device} ===")
            self.diskUsageTab.addItem(f"  Mountpoint: {partition.mountpoint}")
            self.diskUsageTab.addItem(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # jika ada error, di-skip
                self.diskUsageTab.addItem("")
                continue
            self.diskUsageTab.addItem(f"  Total Size: {get_size(partition_usage.total)}")
            self.diskUsageTab.addItem(f"  Used: {get_size(partition_usage.used)}")
            self.diskUsageTab.addItem(f"  Free: {get_size(partition_usage.free)}")
            self.diskUsageTab.addItem(f"  Percentage: {partition_usage.percent}%")
            self.diskUsageTab.addItem("")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        self.diskUsageTab.addItem("Total read:")
        self.diskUsageTab.addItem(f"{get_size(disk_io.read_bytes)}")
        self.diskUsageTab.addItem("")
        self.diskUsageTab.addItem("Total write:")
        self.diskUsageTab.addItem(f"{get_size(disk_io.write_bytes)}")
    
    def jrngInfo(self):
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                self.informasiJaringanTab.addItem(f"=== Interface: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    self.informasiJaringanTab.addItem(f"  IP Address: {address.address}")
                    self.informasiJaringanTab.addItem(f"  Netmask: {address.netmask}")
                    self.informasiJaringanTab.addItem(f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    self.informasiJaringanTab.addItem(f"  MAC Address: {address.address}")
                    self.informasiJaringanTab.addItem(f"  Netmask: {address.netmask}")
                    self.informasiJaringanTab.addItem(f"  Broadcast MAC: {address.broadcast}")
                self.informasiJaringanTab.addItem("")
        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        self.informasiJaringanTab.addItem("Total Bytes Sent:")
        self.informasiJaringanTab.addItem(f"{get_size(net_io.bytes_sent)}")
        self.informasiJaringanTab.addItem("")
        self.informasiJaringanTab.addItem("Total Bytes Received:")
        self.informasiJaringanTab.addItem(f"{get_size(net_io.bytes_recv)}")

        
    
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
