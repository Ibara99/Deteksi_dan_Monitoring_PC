from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, \
     QMessageBox, QInputDialog
from PyQt5 import QtCore
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
def waktu_nyala():
    boot_time_timestamp = psutil.boot_time() #get waktu nyala
    bt = datetime.fromtimestamp(boot_time_timestamp) #ubah format ke datetime
    lama = datetime.now() - bt #selisih waktu sekarang dan waktu nyala
    return str(lama)
    

class Window(QMainWindow, Ui_MainWindow):   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.batasSuhu = 30 #misal, ini nilai default nya ya..

    def initUI(self):
        self.actionSettings.triggered.connect(self.settingFunc)
        self.actionAbout.triggered.connect(self.aboutFunc)
        
        self.systeminfo()
        self.summry()
        self.cpuInfo()
        self.gpuInfo()
        self.mmrInfo()
        self.diskInfo()
        self.jrngInfo()

        #ini untuk Refresh tiap menit
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.readListValues)
        self.timer.start(1000) #1s == 1000 milisecond

    def readListValues(self):
        "Fungsi untuk timer. Bisa dimanfaatkan untuk cek suhu atau semcamnya. \
        semacam scheduler"
        print("")
        uptime = waktu_nyala()
        
        item = self.summaryTab.item(10)
        item.setText(uptime)

        
    def aboutFunc(self):
        QMessageBox.about(
            self,
            "About",
            "<p>Aplikasi untuk mengecek hardware dan spesifikasi laptop</p>"
            "<p>- Juga bakal ada alert, mungkin.</p>"
        )
    def settingFunc(self):
        suhuBaru, ok = QInputDialog.getInt(
                        self, 'Setting Dialog',
                        'Masukkan batas suhu untuk alert: ',
                        self.batasSuhu)
        if ok:
            self.batasSuhu = suhuBaru
    def closeEvent(self, event):
        "fungsi untuk ditrigger ketika aplikasi di-close"
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', 
                         quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.timer.stop()
            event.accept()
        else:
            event.ignore()

    def summry(self):
        try:
            uname = platform.uname()
            os = uname.system
            dvname = uname.node
            phycore = str(psutil.cpu_count(logical=False))
            ttlcore = str(psutil.cpu_count(logical=True))
            cpufreq = psutil.cpu_freq()
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_name = gpu.name
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                list_gpus.append((
                    gpu_name, gpu_total_memory
                ))
            svmem = psutil.virtual_memory()
            partitions = psutil.disk_partitions()
            uptime = waktu_nyala()

            self.summaryTab.addItem("Operating Sistem: ")
            self.summaryTab.addItem(os)
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("Nama Perangkat: ")
            self.summaryTab.addItem(dvname)
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("Lama Waktu PC Menyala: ")
            self.summaryTab.addItem(uptime)
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("==========[ CPU ]==========")
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
            self.summaryTab.addItem("==========[ GPU ]==========")
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("GPU Name :")
            self.summaryTab.addItem(gpu_name)
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("Total Memory :")
            self.summaryTab.addItem(gpu_total_memory)
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("==========[ Memory ]==========")
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("Total Memory")
            self.summaryTab.addItem(f"{get_size(svmem.total)}")
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("Free Memory")
            self.summaryTab.addItem(f"{get_size(svmem.available)}")
            self.summaryTab.addItem(" ")
            self.summaryTab.addItem("==========[ Disk ]==========")
            self.summaryTab.addItem(" ")
            for partition in partitions:
                self.summaryTab.addItem(f"  Disk: {partition.mountpoint}")
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    # jika ada error, di-skip
                    self.summaryTab.addItem("")
                    continue
                self.summaryTab.addItem(f"  Total Size: {get_size(partition_usage.total)}")
                self.summaryTab.addItem("")
        except:
            print("Sepertinya GPU anda tidak terdeteksi")
            pass
        
        
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
            
        cpufreq = psutil.cpu_freq()

        self.cpuTab.addItem("Physical cores : ")
        self.cpuTab.addItem(f"{psutil.cpu_count(logical=False)}")
        self.cpuTab.addItem(" ")
        self.cpuTab.addItem("Total cores : ")
        self.cpuTab.addItem(f"{psutil.cpu_count(logical=True)}")
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
        try:
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                # name of GPU
                gpu_name = gpu.name
                # get % percentage of GPU usage of that GPU
                gpu_load = f"{gpu.load*100}%"
                # get free memory in MB format
                gpu_free_memory = f"{gpu.memoryFree}MB"
                # get used memory
                gpu_used_memory = f"{gpu.memoryUsed}MB"
                # get total memory
                gpu_total_memory = f"{gpu.memoryTotal}MB"
                # get GPU temperature in Celsius
                gpu_temperature = f"{gpu.temperature} °C"
                gpu_uuid = gpu.uuid
                list_gpus.append((
                    gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                    gpu_total_memory, gpu_temperature, gpu_uuid
                ))

            self.gpuTab.addItem("GPU Name :")
            self.gpuTab.addItem(gpu_name)
            self.gpuTab.addItem(" ")
            self.gpuTab.addItem("Load :")
            self.gpuTab.addItem(gpu_load)
            self.gpuTab.addItem(" ")
            self.gpuTab.addItem("Free Memory :")
            self.gpuTab.addItem(gpu_free_memory)
            self.gpuTab.addItem(" ")
            self.gpuTab.addItem("Used Memory :")
            self.gpuTab.addItem(gpu_used_memory)
            self.gpuTab.addItem(" ")
            self.gpuTab.addItem("Total Memory :")
            self.gpuTab.addItem(gpu_total_memory)
            self.gpuTab.addItem(" ")
            self.gpuTab.addItem("Temperature :")
            self.gpuTab.addItem(gpu_temperature)
            self.gpuTab.addItem(" ")
        except:
            print("Sepertinya GPU anda tidak terdeteksi")
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
    win.timer.stop()
    
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook #debug dipanggil di sini
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
    
