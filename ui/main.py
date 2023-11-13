import sys
import signal

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
form_class = uic.loadUiType("./main.ui")[0]

import getdata

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.getData = getdata.GetData()
        self.set_connect()

    def set_connect(self):
        self.ui.open.clicked.connect(self.open)
        self.ui.check.clicked.connect(self.getData.get)
        self.getData.send_img.connect(self.disp_img)
        self.getData.send_nums.connect(self.disp_num)
        self.getData.send_txts.connect(self.disp_txt)

    def open(self):
        path = str(QFileDialog.getExistingDirectory(None, 'Select Directory of top of datasets', QDir.currentPath(),
                                                    QFileDialog.ShowDirsOnly))
        self.getData.set_path(path)

    def disp_img(self, _object):
        self.img.setPixmap(
            QPixmap.fromImage(_object).scaled(self.img.width(), self.img.height(), aspectRatioMode=1))
    
    def disp_num(self, p, v):
        self.p_cnt.setText(str(p))
        self.v_cnt.setText(str(v))
    
    def disp_txt(self, t):
        st = t.split(' ')
        s = st[0:3]+"\n"+st[3:6]+"\n"+st[6:]
        self.caption.setText(s)
    
def signal_handler(sig, frame):
    QApplication.quit()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    app = QApplication(sys.argv)

    try:
        mainWindow = MainWindow()
        mainWindow.showNormal()
        if app.exec_() == 0:
            print()
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        mainWindow.close()
        app.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()