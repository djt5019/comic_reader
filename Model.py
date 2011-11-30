import os

from PySide import QtGui, QtCore

class ImageFile(object):
    def __init__(self, imgPath=None, file=None):
        if imgPath:
            self.image = QtGui.QImage(imgPath)
        else:
            self.image = file

        self.pixmap = QtGui.QPixmap.fromImage(self.image)

        if self.image.isNull():
           print "Unable to load image {}".format(imgPath)

    @property
    def size(self):
        return self.pixmap.size()
    
    @property
    def isNull(self):
        return self.image.isNull()



class Model(object):
    def __init__(self):
        self.scaleFactor = 0.0
        self.images = []
        self.currentImage = 0
        self.numberOfImages = 0
        self.loaderThread = ImageLoaderThread(self.images)
        self.loaderThread.finished.connect(self._getImagesFromThread)

    def hasNextImage(self):
        return self.currentImage != self.numberOfImages-1

    def hasPrevImage(self):
        return self.currentImage != 0

    def loadImages(self, path):
        path = path.lower()
        self.scaleFactor = 1.0
        self.images = []
        self.currentImage = 0
        self.numberOfImages = 0
        self.loaderThread.path = path
        self.loaderThread.images = self.images
        self.loaderThread.start()

    def _getImagesFromThread(self):
        if self.loaderThread.isFinished():
            self.images = self.loaderThread.images
            self.numberOfImages = len(self.images)

    def getNextImage(self):
        if not self.images:
            return None

        if self.currentImage < self.numberOfImages:
            self.currentImage += 1
            return self.images[self.currentImage-1]
        else:
            return self.images[-1]

    def getPrevImage(self):
        if not self.images:
            return None
        
        if self.currentImage > 0:
            self.currentImage -= 1
            return self.images[self.currentImage-1]
        else:
            return self.images[0]

    def zoomImage(self, factor=.25):
        self.scaleFactor *= factor
        img = self.images[self.currentImage]
        img = img.image.scaled(img.size * self.scaleFactor, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        return ImageFile(file=img)

    

class ImageLoaderThread(QtCore.QThread):
    def __init__(self, path=None, images=None, parent=None):
        super(ImageLoaderThread,self).__init__(parent)
        self.images = images
        self.path = path

    #noinspection PyMethodOverriding
    def run(self):
        if not self.path and not self.images:
            return

        if os.path.isdir(self.path):
            self.loadImagesFromDir(self.path)
        else:
            raise FileUnsupported('File type is unsupported')

    def loadImagesFromDir(self, directory=r'C:\Users\Dan\Scripts\python\comic_reader\.idea\imgs\test1'):
        if not os.path.exists(directory):
            return False

        files = os.listdir(directory)
        for f in files:
            if os.path.isfile(os.path.join(directory,f)):
                img = ImageFile(os.path.join(directory,f))
                if not img.isNull:
                    self.images.append(img)


class FileUnsupported(Exception):
    pass