#!/usr/bin/env python
from Model import Model, ImageFile

from PySide import QtCore, QtGui

class View(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.window = Window()
        self.setCentralWidget(self.window)

        self.initActions()
        self.initMenus()

        self.resize(800,600)

    def initActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.showLoadDialog)
        self.exitAct = QtGui.QAction("&Exit", self, shortcut="Ctrl+Q",  triggered=self.close)
        self.aboutAct = QtGui.QAction("&About", self, triggered=self.showHelpDialog)
        self.aboutQtAct = QtGui.QAction("About &Qt", self, triggered=QtGui.qApp.aboutQt)

    def initMenus(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.exitAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.helpMenu)

    def showHelpDialog(self):
        pass

    def showLoadDialog(self):
        fileName = QtGui.QFileDialog.getExistingDirectory(self, 'Open File', QtCore.QDir.currentPath())
        self.window.model.loadImages(fileName)


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.model = Model()
        self.model.imagesLoadedSignal.connect(self.displayImage)

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(False)
        self.imageLabel.resize(800,600)

        self.scrollArea = ScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        self.scrollArea.nextImageSignal.connect(self.nextImage)
        self.scrollArea.prevImageSignal.connect(self.prevImage)

    def nextImage(self):
        self.displayImage(self.model.getNextImage())

    def prevImage(self):
        self.displayImage(self.model.getPrevImage())

    @QtCore.Slot(ImageFile)
    def displayImage(self, img):
        if not img:
            return
        
        if img.image.isNull():
            print "Unable to display {}".format(self.model.currentImage)
            return
        
        print "Displaying {}/{}".format(self.model.currentImage, self.model.numberOfImages)
        self.imageLabel.setPixmap(img.pixmap)
        self.imageLabel.resize(img.size)


class ScrollArea(QtGui.QScrollArea):
    nextImageSignal = QtCore.Signal()
    prevImageSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.buttonDown = False
        self.nextPageCount = 0
        self.prevPageCount = 0

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.buttonDown = True

    def mouseMoveEvent(self, event):
        if self.buttonDown:
            vert = self.verticalScrollBar()
            hori = self.horizontalScrollBar()
            vert.setValue(event.pos().y())
            hori.setValue(event.pos().x())

    def mouseReleaseEvent(self, event):
        self.buttonDown = False

    def wheelEvent(self, event):
        step = event.delta()
        scrollingUp = (event.delta() < 0)

        if event.modifiers() & QtCore.Qt.ControlModifier or self.buttonDown:
            if scrollingUp:
                self.nextImageSignal.emit()
            else:
                self.prevImageSignal.emit()
            event.accept()
            return

        vert = self.verticalScrollBar()
        hori = self.horizontalScrollBar()
        vert.setSingleStep(abs(step))
        hori.setSingleStep(abs(step))

        if scrollingUp:
            if vert.value() == vert.maximum():
                #If we reached the lowest part of the page begin to scroll right
                hori.triggerAction(QtGui.QAbstractSlider.SliderSingleStepAdd)
            else:
                vert.triggerAction(QtGui.QAbstractSlider.SliderSingleStepAdd)
        else:
            if vert.value() == vert.minimum():
                #If we reached the highest part of the page then begin to scroll left
                hori.triggerAction(QtGui.QAbstractSlider.SliderSingleStepSub)
            else:
                vert.triggerAction(QtGui.QAbstractSlider.SliderSingleStepSub)
        
        if vert.value() == vert.maximum() and hori.value() == hori.maximum():
            #If we are at the bottom of the page and keep scrolling down then
            # go to the next page
            if not self.nextPageCount == 2:
                self.nextPageCount += 1
                return

            self.nextImageSignal.emit()
            vert.setValue(vert.minimum())
            hori.setValue(hori.minimum())
            self.nextPageCount = 0
        elif vert.value() == vert.minimum() and hori.value() == hori.minimum():
            #If we are at the top of the page and keep scrolling up then go
            #to the previous page
            if not self.prevPageCount == 2:
                self.prevPageCount += 1
                return

            self.prevImageSignal.emit()
            vert.setValue(vert.maximum())
            hori.setValue(hori.maximum())
            self.prevPageCount = 0
        else:
            self.prevPageCount = 0
            self.nextPageCount = 0

        event.accept()

if __name__ == '__main__':
    app = QtGui.QApplication('app')
    test = View()
    test.show()
    app.exec_()