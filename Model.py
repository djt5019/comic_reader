import os

from PySide import QtGui, QtCore

class ImageFile(object):
    def __init__(self, imgPath):
        self.image = QtGui.QImage(imgPath)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)

        if self.image.isNull():
           print "Unable to load image {}".format(imgPath)

    @property
    def size(self):
        return self.pixmap.size()
    
    @property
    def isNull(self):
        return self.image.isNull()



class Model(QtCore.QObject):
    imagesLoadedSignal = QtCore.Signal((ImageFile,))

    def __init__(self):
        super(Model, self).__init__(None)
        self.images = []
        self.currentImage = 0
        self.numberOfImages = 0

    def loadImages(self, path):
        path = path.lower()
        self.images = []
        self.currentImage = 0
        self.numberOfImages = 0

        if os.path.isdir(path):
            self.loadImagesFromDir(path)
        elif path.endswith('.cbz') or path.endswith('.zip'):
            self.loadImagesFromCbz(path)
        elif path.endswith('.cbr') or path.endswith('rar'):
            self.loadImagesFromCbr(path)
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

        self.numberOfImages = len(self.images)
        self.imagesLoadedSignal.emit(self.images[0])

    def loadImagesFromCbz(self, path):
        pass

    def loadImagesFromCbr(self, path):
        pass

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


class FileUnsupported(Exception):
    pass