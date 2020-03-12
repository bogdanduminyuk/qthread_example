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
    window = QMainWindow()
    ui = MainWindow()

    try:
        ui.setupUi(window)
        window.show()

    except Exception as e:
        QMessageBox.critical(window, "Critical error",
                             str(type(e)) + " " + str(e))
        print(type(e), e)
    else:
        sys.exit(app.exec_())