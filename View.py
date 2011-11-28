#!/usr/bin/env python
import Settings
import os

from PySide import QtCore, QtGui

class View(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.window = Window()
        self.setCentralWidget(self.window)

        self.initSignals()

    def initSignals(self):
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("&Exit the application")
        exitAction.triggered.connect(self.close)

        helpAction = QtGui.QAction('&Info', self)
        helpAction.setShortcut('F1')
        helpAction.setStatusTip("Show help menu")
        helpAction.triggered.connect(self.showHelpDialog)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        helpMenu = menuBar.addMenu('&Help')

        fileMenu.addAction(exitAction)
        helpMenu.addAction(helpAction)

    def showHelpDialog(self):
        pass


class Window(QtGui.QWidget):
    loadImages = QtCore.Signal(str)
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = ScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.scrollArea.nextImage.connect(self.nextImage)
        self.scrollArea.prevImage.connect(self.prevImage)

        self.images = []
        self.numImages = 0
        self.currentImage = 1

        self.loadImagesFromDir()
        self.imageLabel.setGeometry(0,0, 640, 480)

    def loadImagesFromDir(self, directory=r'C:\Users\Dan\Scripts\python\comic_reader\imgs\test'):
        if not os.path.exists(directory):
            return False

        files = os.listdir(directory)
        for f in files:
            #Check Ext
            img = ImageFile(os.path.join(directory,f))
            self.images.append(img)

        self.numImages = len(self.images)
        self.displayImage(self.images[-1])

    def loadImagesFromCbz(self, path):
        pass

    def loadImagesFromCbr(self, path):
        pass

    def nextImage(self):
        if self.currentImage < self.numImages:
            img = self.images[self.currentImage-1]
            self.currentImage += 1
            self.displayImage(img)
        else:
            self.displayImage(self.images[-1])

    def prevImage(self):
        if self.currentImage > 0:
            img = self.images[self.currentImage-1]
            self.currentImage -= 1
            self.displayImage(img)
        else:
            self.displayImage(self.images[0])

    def displayImage(self, img):
        if img.image.isNull():
            return
        print "Displaying {}/{}".format(self.currentImage, self.numImages)
        self.imageLabel.setPixmap(img.pixmap)


class ScrollArea(QtGui.QScrollArea):
    nextImage = QtCore.Signal()
    prevImage = QtCore.Signal()

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)

    def wheelEvent(self, event):
        s = self.verticalScrollBar()
        step = event.delta() / 8
        scrollingUp = event.delta() < 0
        s.setSingleStep(abs(step))

        if event.modifiers() & QtCore.Qt.ControlModifier:
            if scrollingUp:
                self.nextImage.emit()
            else:
                self.prevImage.emit()
            return

        if scrollingUp:
            s.triggerAction(QtGui.QAbstractSlider.SliderSingleStepAdd)
        else:
            s.triggerAction(QtGui.QAbstractSlider.SliderSingleStepSub)

        event.accept()
    

class ImageFile(object):
    def __init__(self, imgPath):
        self.image = QtGui.QImage(imgPath)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)


if __name__ == '__main__':
    app = QtGui.QApplication('app')
    test = View()
    test.show()
    app.exec_()