from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox, QMainWindow

from gui.ui.mainwindow import Ui_MainWindow
from .background import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread = QThread(self)
        self.worker = Worker()

        self.ui.progressBar.setValue(0)

        # connect buttons signals to its slots
        self.ui.pushButton_stop.clicked.connect(self.push_button_stop_click)
        self.ui.pushButton_start.clicked.connect(self.push_button_start_click)

        # now init thread
        self.worker.moveToThread(self.thread)

        # connect button click to worker slot
        # !!! you CAN NOT call thread object "worker" directly
        # so, you have to connect it to any signal in your GUI thread
        self.ui.pushButton_start.clicked.connect(self.worker.do_work)
        self.ui.pushButton_stop.clicked.connect(self.worker.stop)

        self.worker.valueChanged.connect(self.worker_value_changed)
        self.worker.finished.connect(self.worker_work_finished)

    def closeEvent(self, event):
        if not self.thread.isFinished():
            # disable stop with message
            self.worker.finished.disconnect(self.worker_work_finished)

            self.worker.finished.connect(self.stop_thread)
            self.thread.finished.connect(self.close)
            self.ui.pushButton_stop.clicked.emit()

            event.ignore()
        else:
            event.accept()

    def push_button_stop_click(self):
        self.ui.statusbar.showMessage("stop")

    def push_button_start_click(self):
        self.ui.statusbar.showMessage("start")
        self.thread.start()

    def worker_value_changed(self, value):
        self.ui.progressBar.setValue(value)

    def worker_work_finished(self):
        self.stop_thread()
        QMessageBox.information(self, "Information", "Success, your work is done!")

    def stop_thread(self):
        print("stopping thread")
        self.thread.quit()
        self.thread.wait()
