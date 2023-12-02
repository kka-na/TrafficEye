import os
from pathlib import Path
from operator import itemgetter
from collections import Counter

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GetData(QObject):
    def __init__(self):
        super(GetData, self).__init__()
        self.base = ""
        self.data_paths = []
        self.data_len = 0
        self.data_name = ''
        self.now_idx = 0

        self.ci = None
        self.di = None

    send_list = pyqtSignal(object)

    def load_classes(self):
        import clip_inf as ci
        import detect_inf as di

        self.ci = ci
        self.di = di

    def set_path(self, path):
        self.base = str(path)
        self.data_paths.extend(os.path.basename(x)
                                   for x in sorted(Path(path).glob("*.jpg")))
        self.data_len = len(self.data_paths)
        with open(f"{self.base}/classes.txt") as f:
            self.class_list = [line.strip() for line in f.readlines()]
        self.send_list.emit(self.data_paths)
        self.now_data_name = self.data_paths[0].split(".")[0]
        
    send_img = pyqtSignal(object)
    send_tr_img = pyqtSignal(object)
    send_tr_type = pyqtSignal(int)
    send_nums = pyqtSignal(int, int)
    send_txts = pyqtSignal(str)
    send_inf = pyqtSignal(str, int)

    def get(self):
        data_path = f"{self.base}/{self.now_data_name}.jpg"
        qimg = QImage(data_path)
        self.send_img.emit(qimg)
        QCoreApplication.processEvents()
        
        self.width = qimg.width()
        self.height = qimg.height()

        #inf_path = f"{self.base}/{self.now_data_name}_cls.txt"
        # cap_path = f"{self.base}/{self.now_data_name}_cap.txt"
        inf_list = self.di.get_result(data_path)

        bboxes = self.get_label_list(inf_list)
        tr = self.get_tr_img(qimg, bboxes)
        if tr != None:
            self.send_tr_type.emit(tr[0])
            self.send_tr_img.emit(tr[1])

        img = self.draw_boxes(qimg, bboxes)
        self.send_img.emit(img)

        p, v = self.get_target_num_of_cls(bboxes)
        self.send_nums.emit(p, v)

        # with open(cap_path, 'r') as f:
        #     cap = f.readline()
        cap = self.ci.get_result(data_path)
        print(QObjectCleanupHandler)
        self.send_txts.emit(cap)
        

    def get_label_list(self, inf_list):
        bboxes = []
        for line in inf_list:
            val = line.split(' ')
            if len(val) == 5:
                conf = 1.0
                calc_box = self.calc_boxes(val[1:])
                _center = [float(val[1]) * self.width,
                            float(val[2]) * self.height]
            else:
                conf = float(val[1])
                calc_box = self.calc_boxes(val[2:])
                _center = [float(val[2]) * self.width,
                            float(val[3]) * self.height]
            bbox = {'cls': val[0], 'conf': conf, 'size': calc_box[0:2],
                    'bbox': calc_box[2:], 'center': _center}
            bboxes.append(bbox)

        bboxes = sorted(bboxes, key=itemgetter('conf'), reverse=True)
        return bboxes

    def calc_boxes(self, _object):
        lx = (float(_object[0]) - float(_object[2]) / 2) * self.width
        ly = (float(_object[1]) - float(_object[3]) / 2) * self.height
        rx = (float(_object[0]) + float(_object[2]) / 2) * self.width
        ry = (float(_object[1]) + float(_object[3]) / 2) * self.height
        return [float(_object[2]) * self.width, float(_object[3]) * self.height, lx, ly, rx, ry]


    def get_target_num_of_cls(self, bboxes, p=0, v=2):
        cls_counts = Counter(int(bbox['cls']) for bbox in bboxes)
        return cls_counts[p], cls_counts[v]

    def draw_boxes(self, img, bboxes):
        if len(bboxes) > 0:
            painter = QPainter(img)
            f = QFont("Helvetica [Cronyx]", img.height() / 30)
            for i, bbox in enumerate(bboxes):
                pen = self.get_bbox_pen(int(bbox['cls']))
                painter.setPen(pen)
                qrect = QRect(bbox['bbox'][0], bbox['bbox'][1], bbox['size'][0], bbox['size'][1])
                painter.drawRect(qrect)
                painter.setFont(f)
                class_name = self.class_list[int(bbox['cls'])]
                painter.drawText(
                    bbox['bbox'][0], bbox['bbox'][1] - 10, class_name)
            painter.end()
        return img
    
    def get_tr_img(self, image, bboxes, tr=[9]):
        best_bbox = {}
        best_conf = 0
        for i, bbox in enumerate(bboxes):
            if int(bbox['cls']) in tr:
                if float(bbox['conf']) >best_conf:
                    best_bbox = bbox
                    best_conf = float(bbox['conf'])
        if best_bbox:
            best_rect = QRect(best_bbox['bbox'][0], best_bbox['bbox'][1], best_bbox['size'][0], best_bbox['size'][1])
            tr_img = self.crop_image(image, best_rect)
            tr_type = int(best_bbox['cls'])
            return tr_type, tr_img
        else:
            return None

    def crop_image(self, image, crop_rect):
        cropped_pixmap = QPixmap(crop_rect.size())
        cropped_pixmap.fill(Qt.white)
        painter = QPainter(cropped_pixmap)

        painter.drawPixmap(QRect(0, 0, crop_rect.width(), crop_rect.height()), QPixmap.fromImage(image), crop_rect)
        painter.end()
        return cropped_pixmap
    
    def get_bbox_pen(self, _object):
        pen = QPen()
        pen.setWidth(3)
        if _object % 6 == 0:
            qb = QBrush(QColor('#fcb711'))
            pen.setBrush(qb)
        elif _object % 6 == 1:
            qb = QBrush(QColor('#6460aa'))
            pen.setBrush(qb)
        elif _object % 6 == 2:
            qb = QBrush(QColor('#cc004c'))
            pen.setBrush(qb)
        elif _object % 6 == 3:
            qb = QBrush(QColor('#0db14b'))
            pen.setBrush(qb)
        elif _object % 6 == 4:
            qb = QBrush(QColor('#0089d0'))
            pen.setBrush(qb)
        else:
            qb = QBrush(QColor('#f37021'))
            pen.setBrush(qb)
        return pen

    def move(self, idx):
        self.now_idx += idx
        if self.now_idx < 0:
            self.now_idx = 0
        elif self.now_idx > self.data_len - 1:
            self.now_idx = self.data_len - 1
        self.now_data_name = self.data_paths[self.now_idx].split(".")[0]
        self.send_inf.emit(self.now_data_name, self.now_idx)
        QCoreApplication.processEvents()
        self.get()
    
    def change(self, idx):
        self.now_idx = idx
        self.now_data_name = self.data_paths[self.now_idx].split(".")[0]
        self.send_inf.emit(self.now_data_name, self.now_idx)
        QCoreApplication.processEvents()
        self.get()