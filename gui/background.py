import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication


class Worker(QObject):
    finished = pyqtSignal()
    valueChanged = pyqtSignal(int)

    def __init__(self):
        super(Worker, self).__init__()
        self.value = None
        self.stop_trigger = None

    def do_work(self):
        self.value = 0
        self.stop_trigger = False

        for i in range(1000000000):
            if self.stop_trigger:
                break

            self.value += 1
            time.sleep(1)
            self.valueChanged.emit(self.value)

            QApplication.processEvents()

        self.finished.emit()

    @pyqtSlot()
    def stop(self):
        print("stop slot")
        self.stop_trigger = True
