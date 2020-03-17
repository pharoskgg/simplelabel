import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QFileDialog,
                             QListWidget, QGraphicsView, QMessageBox, QLabel, QPushButton, QComboBox)
from PyQt5.QtGui import QIcon, QImage, QPixmap

class Example(QMainWindow):
    def __init__(self):
        self.index = 0
        self.count = 0
        # 保存图片的路径
        self.savePath = r'G:\DeepLearning\detectcarproject\data\colorLabel'
        # 打开文件的默认路径
        self.openImagePath = r'G:\DeepLearning\detectcarproject\data\images'
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(831, 641)
        #设置菜单文件功能
        openDirectAction = QAction('Open',self)
        openDirectAction.setStatusTip('打开文件夹里面的图片')
        openDirectAction.triggered.connect(self.openDirect)

        # 设置菜单栏
        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(openDirectAction)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 26))

        #创建listwiget
        self.listwidget = QListWidget(self)
        self.listwidget.setGeometry(QtCore.QRect(0, 27, 261, 591))
        self.listwidget.itemClicked.connect(self.listClicked)
        self.listwidget.currentItemChanged.connect(self.listClicked)

        # 图片切换按钮
        # 前一张
        self.bt_previous = QPushButton('Previous', self)
        self.bt_previous.setShortcut('a')
        self.bt_previous.setGeometry(QtCore.QRect(268, 550, 91, 61))
        self.bt_previous.clicked.connect(self.previousClicked)
        # 后一张
        self.bt_next = QPushButton('Next', self)
        self.bt_next.setShortcut('d')
        self.bt_next.setGeometry(QtCore.QRect(730, 550, 91, 61))
        self.bt_next.clicked.connect(self.nextClicked)

        # 图片
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.setGeometry(QtCore.QRect(320, 27, 450, 450))

        # 标签选择
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(500, 480, 101,21)
        self.comboBox.addItem("黑色")
        self.comboBox.addItem("白色")
        self.comboBox.addItem("银灰色")
        self.comboBox.addItem("蓝色")
        self.comboBox.addItem("红色")
        self.comboBox.addItem("绿色")
        self.comboBox.addItem("黄色")

        self.comboBox

        # 保存标签按钮
        self.bt_save = QPushButton('Save', self)
        self.bt_save.setShortcut('s')
        self.bt_save.setGeometry(QtCore.QRect(500, 550, 91, 61))
        self.bt_save.clicked.connect(self.saveClicked)


        # 设置窗口标题
        self.setWindowTitle('Color-Label')
        self.show()
    
    # 单击文件打开事件
    def openDirect(self):
        path = QFileDialog.getExistingDirectory(self, 'Open file', self.openImagePath)
        count = -1
        for i in os.listdir(path):
            if (str(i).split('.')[-1] == 'png') or (str(i).split('.')[-1] == 'jpg'):
                self.listwidget.addItem(path+'/'+i)
                count += 1
        self.count = count
        self.listwidget.setCurrentRow(self.index)
    
    # 单击ListviewItem事件和焦点事件
    def listClicked(self, Index):
        path = self.listwidget.item(self.listwidget.row(Index)).text()
        self.image.setPixmap(QPixmap(path))
        # 获取选中行的索引值
        self.index = self.listwidget.selectedIndexes()[0].row()
        self.statusBar().showMessage(path)

    # 前一张图片
    def previousClicked(self):
        # self.listwidget.nextInFocusChain()
        if self.index > 0:
            self.index -= 1
            self.updateFocus()

    # 后一张图片
    def nextClicked(self):
        if self.index < self.count:
            self.index += 1
            self.updateFocus()

    def updateFocus(self):
        self.listwidget.setCurrentRow(self.index)

    # 保存标签
    def saveClicked(self):
        print(self.listwidget.item(self.index).text())
        # 获得图片名字，颜色标签
        fileName = self.listwidget.item(self.index).text()
        # 取得整个文件名
        fullFileName = fileName.split('/')[-1]
        # 去掉后缀名
        fileName = fullFileName.split('.')[0]
        # print(fileName)
        # 生成保存文件的路径
        savePath = self.savePath + '\\' + fileName+'.txt'
        with open(savePath,'w') as f:
            f.write(fileName + ' '+ str(self.comboBox.currentIndex())+'\n')
            self.statusBar().showMessage('保存成功:'+fullFileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())