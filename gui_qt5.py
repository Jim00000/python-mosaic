# -*- coding:utf-8 -*-
'''
    File name: gui_qt5.py
    Author   : Jim00000 <good0121good@gmail.com>
'''

import sys
from qt5.gui_main import MosaicGUI
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MosaicGUI()
    sys.exit(app.exec_())