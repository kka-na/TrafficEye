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
        self.tr_list = [self.t1, self.t2, self.t3, self.t4]
        self.open.clicked.connect(self.set)
        self.getData.send_list.connect(self.disp_list)
        self.check.clicked.connect(self.getData.get)
        self.up.clicked.connect(self.go_up)
        self.down.clicked.connect(self.go_down)
        self.getData.send_img.connect(self.disp_img)
        self.getData.send_tr_img.connect(self.disp_tr_img)
        self.getData.send_tr_type.connect(self.disp_tr_type)
        self.getData.send_nums.connect(self.disp_num)
        self.getData.send_txts.connect(self.disp_txt)

    def set(self):
        path = str(QFileDialog.getExistingDirectory(None, 'Select Directory of top of datasets', QDir.currentPath(),
                                                    QFileDialog.ShowDirsOnly))
        self.getData.set_path(path)

    def disp_list(self, _object):
        for i in _object:
            item = QListWidgetItem(i)
            self.list.addItem(item)
        self.data_len = self.getData.data_len

    def disp_img(self, _object):
        self.img.setPixmap(
            QPixmap.fromImage(_object).scaled(self.img.width(), self.img.height(), aspectRatioMode=1))
    
    def disp_tr_img(self, _object):
        self.tr_img.setPixmap(_object.scaled(self.img.width(), self.img.height(), aspectRatioMode=1))
    
    def disp_tr_type(self, t):
        #TODO fix tr class (9) -> for test
        tl_cls_list = [[9, 6, 12, 10,13, 15], [8, 11, 13, 16], [12, 14], [4, 14, 17]] #R, Y, Arr, G
        tl_detect_cls = [i for i, cls in enumerate(tl_cls_list) if t in cls]
        
        for tc in tl_detect_cls:
            if tc == 0:
                self.tr_list[tc].setStyleSheet('border:1px solid black;border-radius:25px;background-color: rgb(255, 66, 98);')
            if tc == 1:
                self.tr_list[tc].setStyleSheet('border:1px solid black;border-radius:25px;background-color: rgb(255, 208, 66);')
            if tc == 2 or tc == 3:
                self.tr_list[tc].setStyleSheet('border:1px solid black;border-radius:25px;background-color: rgb(59, 217, 153);')
        
    def disp_num(self, p, v):
        self.p_cnt.setText(str(p))
        self.v_cnt.setText(str(v))
    
    def disp_txt(self, t):
        st = t.split(' ')
        s = ' '.join(st[0:3])+"\n"+' '.join(st[3:6])+"\n"+' '.join(st[6:])
        self.caption.setText(s)
    
    def go_up(self):
        self.getData.move(-1)

    def go_down(self):
        self.getData.move(1)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showNormal()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()