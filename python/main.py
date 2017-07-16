
import sys
import os
import binascii
import time

import serial
import serial.tools.list_ports
from PyQt5 import QtGui, QtWidgets, QtCore
import numpy as np

# version check
from platform import python_version
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR
print("## python ",python_version())
print("## Qt     ",QT_VERSION_STR)
print("## PyQt   ",PYQT_VERSION_STR)
print("## sip    ",SIP_VERSION_STR)
# assert(python_version() == '3.5.2')
# assert(QT_VERSION_STR == '5.6.2')
# assert(PYQT_VERSION_STR == '5.6')
# assert(SIP_VERSION_STR == '4.18')

from gui import main_window


size_list = []
size_head =      ['Name' , 'w', 'h']
size_list.append(['QQVGA', 160, 120])
size_list.append(['QVGA' , 320, 240])
size_list.append(['VGA'  , 640, 480])

mode_list = []
mode_head =      ['Name'      ,'d', 'QtFormat']
mode_list.append(['Grayscale8', 1,  QtGui.QImage.Format_Grayscale8])
mode_list.append(['RGB444'    , 2,  QtGui.QImage.Format_RGB444])


class MainForm(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.pixitem = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixitem)
        self.graphicsView.setScene(self.scene)

        self.reciever = Reciever()
        self.reciever.signalObject.connect(self.update_image)

        self.buf_list = []

        #
        # self.test()
        self.reciever.setup(self.buf_list)
        self.reciever.start()

    def update_image(self):
        buf=self.buf_list.pop(0)
        print('update_image')
        print(buf[0:1],buf[-8:])

        size_dict = dict(zip(size_head, size_list[1]))
        mode_dict = dict(zip(mode_head, mode_list[0]))
        w=size_dict['w']
        h=size_dict['h']
        d=mode_dict['d']
        qt_format = mode_dict['QtFormat']

        if buf[0:1]!=b'\xff': return # header
        if buf[-8:]!=b'\x00\x00\x00\x00\x00\x00\x00\x00': return # footer
        print(len(buf[1:-8]))
        # assert(len(buf[1:-8])==h*w)
        # self.image = np.fromstring(buf[1:-8], dtype=np.uint8)
        self.qimage = QtGui.QImage(buf[1:-8], w, h, w*d, qt_format)
        self.pixmap = QtGui.QPixmap.fromImage(self.qimage)
        self.pixitem.setPixmap(self.pixmap)

    # def test(self):
    #     h=240
    #     w=320
    #     d=2   # 2*uint8 :2byte:16bitRGB
    #     image=np.zeros((h,w,d), dtype='uint8')
    #
    #     for i in range(h):
    #         for j in range(w):
    #             r = int(i*0b1111/h)
    #             g = int(j*0b1111/w)
    #             b = int(0)
    #             image[i,j,0] = g << 4 | b
    #             image[i,j,1] = 0 << 4 | r
    #
    #     self.qimage = QtGui.QImage(image.data, w, h, w*d, QtGui.QImage.Format_RGB444)
    #     self.pixmap = QtGui.QPixmap.fromImage(self.qimage)
    #     self.pixitem.setPixmap(self.pixmap)



class Reciever(QtCore.QThread):
    signalObject = QtCore.pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.stopped = False
        self.mutex = QtCore.QMutex()

    def setup(self, buf_list):
        self.buf_list = buf_list
        self.stopped = False

    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True

    def run(self):
        usbserial_names = serial.tools.list_ports.comports()
        usbserial_names = list(filter(lambda x: x[2]!='n/a', usbserial_names ))
        self.usbserial = serial.Serial(usbserial_names[0][0], 1000000)

        buf=[]
        while True:
            tmp = self.usbserial.read(self.usbserial.inWaiting())
            if len(tmp)!=0:
                buf.append(tmp)
            if tmp.endswith(b'\x00\x00\x00\x00\x00\x00\x00\x00'):
                self.mutex.lock()
                self.buf_list.append(b''.join(buf))
                buf=[]
                # print(self.buf_list[-1], len(self.buf_list[-1]))
                self.mutex.unlock()
                self.signalObject.emit()

        self.stop()
        self.finished.emit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    app.exec_()

if __name__ == '__main__':
    main()
