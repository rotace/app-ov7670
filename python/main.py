
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

        self.lineEdit_send.returnPressed.connect(self.send_command)

        self.receiver = Receiver()
        self.receiver.signalReceiveImg.connect(self.update_image)
        self.receiver.signalReceiveTxt.connect(self.receive_text)

        self.imgbuf_list = []

        #
        # self.test()
        self.receiver.setup(self.imgbuf_list)
        self.receiver.start()

    def send_command(self):
        print("send command")
        command = self.lineEdit_send.text()
        command += "\n"
        command = command.replace(" ", "")
        self.receiver.send_command(command)
        self.lineEdit_send.clear()
        self.lineEdit_send.setEnabled(False)

    def receive_text(self, text):
        print("receive text")
        self.lineEdit_receive.setText(text)
        self.lineEdit_send.setEnabled(True)

    def update_image(self):
        imgbuf=self.imgbuf_list.pop(0)

        size_dict = dict(zip(size_head, size_list[1]))
        mode_dict = dict(zip(mode_head, mode_list[1]))
        w=size_dict['w']
        h=size_dict['h']
        d=mode_dict['d']
        qt_format = mode_dict['QtFormat']

        print('updating image, size=' + str(len(imgbuf)) )
        if len(imgbuf) != w*h*d:
            return

        self.qimage = QtGui.QImage(imgbuf, w, h, w*d, qt_format)
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



class Receiver(QtCore.QThread):
    signalReceiveImg = QtCore.pyqtSignal()
    signalReceiveTxt = QtCore.pyqtSignal( str )

    def __init__(self):
        super(self.__class__, self).__init__()
        self.stopped = False
        self.has_cmd = False
        self.is_txt = False
        self.is_img = True
        self.command = ""
        self.mutex = QtCore.QMutex()

    def setup(self, imgbuf_list):
        self.imgbuf_list = imgbuf_list
        self.stopped = False

    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stopped = True

    def send_command(self, command):
        self.command = command
        self.has_cmd = True

    def run(self):
        usbserial_names = serial.tools.list_ports.comports()
        usbserial_names = list(filter(lambda x: x[2]!='n/a', usbserial_names ))
        self.usbserial = serial.Serial(usbserial_names[0][0], 1000000)

        imgbuf=[]
        txtbuf=[]
        while True:
            if self.usbserial.inWaiting()==0:
                if not(self.is_img) and not(self.is_txt) and self.has_cmd:
                    self.usbserial.write(self.command.encode('utf-8'))
                    print(self.command)
                    self.command=""
                    self.has_cmd=False
                continue

            # print(self.usbserial.inWaiting())
            tmp = self.usbserial.read(self.usbserial.inWaiting())

            while len(tmp):
                if not(self.is_txt) and not(self.is_img):
                    if tmp.startswith(b'\x02'):
                        print("getting text")
                        self.is_txt=True
                        tmp=tmp[1:]
                        continue
                    elif tmp.startswith(b'\x00\xff\x00\x00\xff\x00\x00\xff\x00'):
                        print("getting image")
                        self.is_img=True
                        tmp=tmp[9:]
                        continue
                    else:
                        index = tmp.find(b'\x00\xff\xff\x00\xff\xff\x00\xff\xff')
                        if index==-1:
                            break
                        else:
                            tmp=tmp[index+1:]
                            continue

                elif self.is_txt and not(self.is_img):
                    index = tmp.find(b'\x03')
                    if index==-1:
                        txtbuf.append(tmp)
                        break
                    else:
                        txtbuf.append(tmp[0:index])
                        print(b''.join(txtbuf))
                        self.signalReceiveTxt.emit(b''.join(txtbuf).decode('utf-8'))
                        txtbuf=[]
                        self.is_txt=False
                        tmp=tmp[index+1:]
                        continue

                elif self.is_img and not(self.is_txt):
                    index = tmp.find(b'\x00\xff\xff\x00\xff\xff\x00\xff\xff')
                    if index==-1:
                        imgbuf.append(tmp)
                        break
                    else:
                        imgbuf.append(tmp[0:index])
                        self.mutex.lock()
                        self.imgbuf_list.append(b''.join(imgbuf))
                        self.mutex.unlock()
                        self.signalReceiveImg.emit()
                        # print(b''.join(imgbuf))
                        imgbuf=[]
                        self.is_img=False
                        tmp=tmp[index+9:]
                        continue

                else:
                    assert(False)

        self.stop()
        self.finished.emit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    app.exec_()

if __name__ == '__main__':
    main()
