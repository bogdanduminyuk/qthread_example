import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui.mainwindow import MainWindow


def get_platforms_path():
    file_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        file_path, 'venv', 'Lib', 'site-packages', 'PyQt5', 'Qt', 'plugins', 'platforms'
    )


if __name__ == '__main__':
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = get_platforms_path()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
