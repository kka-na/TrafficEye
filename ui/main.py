import sys

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
        self.open.clicked.connect(self.set)
        self.check.clicked.connect(self.getData.get)
        self.getData.send_img.connect(self.disp_img)
        self.getData.send_nums.connect(self.disp_num)
        self.getData.send_txts.connect(self.disp_txt)

    def set(self):
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
        s = ' '.join(st[0:3])+"\n"+' '.join(st[3:6])+"\n"+' '.join(st[6:])
        self.caption.setText(s)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showNormal()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()