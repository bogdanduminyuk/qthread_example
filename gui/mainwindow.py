from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

from gui.ui.mainwindow import Ui_MainWindow
from .background import Worker


class MainWindow(Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.window = None
        self.thread = None
        self.worker = Worker()

    def setupUi(self, window):
        self.window = window
        self.thread = QThread(window)

        super(MainWindow, self).setupUi(window)

        self.progressBar.setValue(0)

        # connect buttons signals to its slots
        self.pushButton_stop.clicked.connect(self.push_button_stop_click)
        self.pushButton_start.clicked.connect(self.push_button_start_click)

        # now init thread
        self.worker.moveToThread(self.thread)

        # connect button click to worker slot
        # !!! you CAN NOT call thread object "worker" directly
        # so, you have to connect it to any signal in your GUI thread
        self.pushButton_start.clicked.connect(self.worker.do_work)
        self.pushButton_stop.clicked.connect(self.worker.stop)

        self.worker.valueChanged.connect(self.worker_value_changed)
        self.worker.finished.connect(self.worker_work_finished)

    def push_button_stop_click(self):
        self.statusbar.showMessage("stop")

    def push_button_start_click(self):
        self.statusbar.showMessage("start")
        self.thread.start()

    def worker_value_changed(self, value):
        self.progressBar.setValue(value)

    def worker_work_finished(self):
        self.stop_thread()
        QMessageBox.information(self.window, "Information", "Success, your work is done!")

    def stop_thread(self):
        self.thread.quit()
        self.thread.wait()
