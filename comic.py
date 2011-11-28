from PySide import QtGui
from View import CreateView

def main():
    app = QtGui.QApplication('App')
    prg = CreateView()
    prg.show()
    return app.exec_()
    
if __name__ == '__main__':
    main()
    