import sys
import time
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
        QTimer.singleShot(100, self.class_loading)

    def class_loading(self):
        loading_start = time.time()
        self.getData.load_classes()
        elapsed_time = time.time()-loading_start
        self.loading.setText(f"{elapsed_time:.3f} sec")
        self.loading.setStyleSheet('color:rgb(38, 121, 255)')
        self.set_connect()


    def set_connect(self):
        self.tr_list = [self.t1, self.t2, self.t3, self.t4]
        self.open.clicked.connect(self.set)
        self.getData.send_list.connect(self.disp_list)
        self.up.clicked.connect(self.go_up)
        self.down.clicked.connect(self.go_down)
        self.getData.send_img.connect(self.disp_img)
        self.getData.send_tr_img.connect(self.disp_tr_img)
        self.getData.send_tr_type.connect(self.disp_tr_type)
        self.getData.send_nums.connect(self.disp_num)
        self.getData.send_txts.connect(self.disp_txt)
        self.getData.send_inf.connect(self.disp_inf)
    

    def check_start(self):
        check_start = time.time()
        self.getData.get()
        elpased_time = time.time() - check_start
        self.inference.setText(f"{elpased_time:.3f} sec")
        self.inference.setStyleSheet('color:rgb(255, 38, 121)')


    def set(self):
        path = str(QFileDialog.getExistingDirectory(None, 'Select Directory of top of datasets', QDir.currentPath(),
                                                    QFileDialog.ShowDirsOnly))
        self.getData.set_path(path)
        self.check_start()
        
    def disp_list(self, _object):
        for i in _object:
            item = QListWidgetItem(i)
            self.list.addItem(item)
        self.data_len = self.getData.data_len

        self.disp_inf(_object[0], 0)
        l = QListWidget()
        self.list.itemClicked.connect(self.list_changes)            
        
    def init_txts(self):
        self.inference.setText("Inferencing ...")
        self.inference.setStyleSheet('color:rgb(0,0,0)')
        self.caption.setText('Caption')

    def list_changes(self):

        self.init_txts()
        self.init_trafficlight()
        QCoreApplication.processEvents()
        check_start = time.time()
        self.getData.change(self.list.currentRow())
        elpased_time = time.time() - check_start
        self.inference.setText(f"{elpased_time:.3f} sec")
        self.inference.setStyleSheet('color:rgb(255, 38, 121)')

        
    def disp_img(self, _object):
        self.img.setPixmap(
            QPixmap.fromImage(_object).scaled(self.img.width(), self.img.height(), aspectRatioMode=1))
        QCoreApplication.processEvents()
    
    def disp_tr_img(self, _object):
        self.tr_img.setPixmap(_object.scaled(self.tr_img.width(), self.tr_img.height(), aspectRatioMode=1))
    
    def init_trafficlight(self):
        for t in self.tr_list:
            t.setStyleSheet('border:1px solid black; border-radius:40px; background-color: rgb(243,243, 243); color:rgb(243, 243, 243);')
        px = QPixmap(self.tr_img.width(), self.tr_img.height())
        px.fill(Qt.transparent)
        self.tr_img.setPixmap(px)
    
    def disp_tr_type(self, t):
        #tc = R, Y, Arr, G

        def turn_red():
            self.tr_list[0].setStyleSheet('border:1px solid black;border-radius:40px;background-color: rgb(255, 66, 98);')
        
        def turn_yellow():
            self.tr_list[1].setStyleSheet('border:1px solid black;border-radius:40px;background-color: rgb(255, 208, 66);')
        
        def turn_green_arr(tc):
            self.tr_list[tc].setStyleSheet('border:1px solid black;border-radius:40px;background-color: rgb(35, 232, 120); color:rgb(243, 243, 243);')

        green = [4,9]
        red = [6,10]
        yellow = [8,11]
        red_arrow = 12
        red_yellow = 13
        green_arrow = 14
        black = 18

        if t in green:
            turn_green_arr(3)
        elif t in red:
            turn_red()
        elif t in yellow:
            turn_yellow()
        elif t == red_arrow:
            turn_red()
            turn_green_arr(2)
        elif t==red_yellow:
            turn_red()
            turn_yellow()
        elif t==green_arrow:
            turn_green_arr(2)
            turn_green_arr(3)
        elif t==black:
            self.init_trafficlight()


        
    def disp_num(self, p, v):
        self.p_cnt.setText(str(p))
        self.v_cnt.setText(str(v))
    
    def disp_txt(self, t):
        st = t.split(' ')
        s = ' '.join(st[0:3])+"\n"+' '.join(st[3:6])+"\n"+' '.join(st[6:])
        self.caption.setText(s)
    
    def disp_inf(self, t, i):
        self.file.setText(t)
        self.list.setCurrentRow(i)

    
    def go_up(self):
        self.init_txts()
        self.init_trafficlight()
        QCoreApplication.processEvents()
        check_start = time.time()
        self.getData.move(-1)
        elpased_time = time.time() - check_start
        self.inference.setText(f"{elpased_time:.3f} sec")
        self.inference.setStyleSheet('color:rgb(255, 38, 121)')

    def go_down(self):
        self.init_txts()
        self.init_trafficlight()
        QCoreApplication.processEvents()
        check_start = time.time()
        self.getData.move(1)
        elpased_time = time.time() - check_start
        self.inference.setText(f"{elpased_time:.3f} sec")
        self.inference.setStyleSheet('color:rgb(255, 38, 121)')

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showNormal()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()