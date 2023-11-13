import os
from operator import itemgetter
from collections import Counter

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GetData(QObject):
    def __init__(self):
        super(GetData, self).__init__()
        self.base = ""

    def set_path(self, path):
        self.base = str(path)
        with open(f"{self.base}/classes.txt") as f:
            self.class_list = [line.strip() for line in f.readlines()]

    send_img = pyqtSignal(object)
    send_nums = pyqtSignal(int, int)
    send_txts = pyqtSignal(str)

    def get(self):
        data_path = f"{self.base}/img.jpg"
        img = QImage(data_path)
        self.width = img.width()
        self.height = img.height()

        inf_path = f"{self.base}/inf_cls.txt"
        cap_path = f"{self.base}/inf_cap.txt"

        bboxes = self.get_label_list(inf_path)
        img = self.draw_boxes(img, bboxes)
        self.send_img.emit(img)
        p, v = self.get_target_num_of_cls(bboxes)
        self.send_nums.emit(p, v)
        with open(cap_path, 'r') as f:
            cap = f.readline()
        self.send_txts.emit(cap)
        

    def get_label_list(self, file):
        bboxes = []
        if os.path.isfile(file):
            fr = open(file)
            lines = fr.readlines()
            for line in lines:
                val = line.split()
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
            f = QFont("Helvetica [Cronyx]", img.height() / 50)
            for bbox in bboxes:
                pen = self.get_bbox_pen(int(bbox['cls']))
                painter.setPen(pen)
                qrect = QRect(bbox['bbox'][0], bbox['bbox']
                              [1], bbox['size'][0], bbox['size'][1])
                painter.drawRect(qrect)
                painter.setFont(f)
                class_name = self.class_list[int(bbox['cls'])]
                painter.drawText(
                    bbox['bbox'][0], bbox['bbox'][1] - 10, class_name)
            painter.end()
        return img

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