# -*- coding:utf-8 -*-
'''
    File name: gui_main.py
    Author   : Jim00000
'''

import sys
import os
import platform
import _thread
import shutil
from PyQt5.QtCore import Qt, QThread, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, \
                            QPushButton, QGridLayout, QFileDialog, QLCDNumber, \
                            QSlider, QRadioButton, QCheckBox, QMessageBox, QProgressBar, \
                            QVBoxLayout

class MosaicGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.__init_element__()
        self.__init_layout__()
        self.__init_event__()
        self.resize(400, 400)
        self.setWindowTitle('Mosaic convertor')
        self.show()

    def __init_element__(self):
        self.statusBar()
        self.setFont(QFont("Times", 12))

        self.input_label = QLabel('Image path : ', self)
        self.input_editor = QLineEdit(self)
        self.input_btn = QPushButton('Load', self)

        self.input_err_rate_label = QLabel('Error rate : ', self)
        self.input_err_rate = QLCDNumber(self)
        self.input_err_rate.display(0.5)
        self.input_err_rate_slider = QSlider(Qt.Horizontal, self)
        self.input_err_rate_slider.setRange(1, 1000)
        self.input_err_rate_slider.setValue(500)

        self.input_min_area_label = QLabel('Min pixel : ', self)
        self.input_min_area = QLCDNumber(self)
        self.input_min_area.display(64)
        self.input_min_area_slider = QSlider(Qt.Horizontal, self)
        self.input_min_area_slider.setRange(1, 8)
        self.input_min_area_slider.setValue(3)
        self.input_min_area_slider.setTickPosition(QSlider.TicksBelow)
        self.input_min_area_slider.setTickInterval(1)

        self.iter_label = QLabel('Iteration : ', self)
        self.iter_value = QLCDNumber(self)
        self.iter_value.display(3)
        self.iter_slider = QSlider(Qt.Horizontal, self)
        self.iter_slider.setRange(1, 10)
        self.iter_slider.setValue(3)
        self.iter_slider.setTickPosition(QSlider.TicksBelow)
        self.iter_slider.setTickInterval(1)

        self.plot_average_radbtn = QRadioButton("Average color")
        self.plot_average_radbtn.setChecked(True)
        self.plot_centroidal_radbtn = QRadioButton("Centroidal color")
        self.plot_edge = QCheckBox("Plot edges")

        self.generate_btn = QPushButton("Generate")
        self.progress = QProgressBar(self)

    def __init_layout__(self):

        vbox = QVBoxLayout()
        grid = QGridLayout()

        grid.addWidget(self.input_label, 0, 0, Qt.AlignTop)
        grid.addWidget(self.input_editor, 0, 1, Qt.AlignTop)
        grid.addWidget(self.input_btn, 0, 2, Qt.AlignTop)

        grid.addWidget(self.input_err_rate_label, 1, 0, Qt.AlignTop)
        grid.addWidget(self.input_err_rate, 1, 1, Qt.AlignTop)
        grid.addWidget(self.input_err_rate_slider, 1, 2, Qt.AlignTop)

        grid.addWidget(self.input_min_area_label, 2, 0, Qt.AlignTop)
        grid.addWidget(self.input_min_area, 2, 1, Qt.AlignTop)
        grid.addWidget(self.input_min_area_slider, 2, 2, Qt.AlignTop)

        grid.addWidget(self.iter_label, 3, 0, Qt.AlignTop)
        grid.addWidget(self.iter_value, 3, 1, Qt.AlignTop)
        grid.addWidget(self.iter_slider, 3, 2, Qt.AlignTop)

        grid.addWidget(self.plot_average_radbtn, 4, 0, Qt.AlignTop)
        grid.addWidget(self.plot_centroidal_radbtn, 4, 1, Qt.AlignTop)
        grid.addWidget(self.plot_edge, 4, 2, Qt.AlignTop)

        vbox.addLayout(grid)
        vbox.addWidget(self.generate_btn)
        vbox.addWidget(self.progress)

        self.widget.setLayout(vbox)

    def __init_event__(self):
        self.input_btn.clicked.connect(self.__clicked_load__)
        self.input_err_rate_slider.valueChanged.connect(self.__err_value_changed__)
        self.input_min_area_slider.valueChanged.connect(self.__min_area_changed__)
        self.iter_slider.valueChanged.connect(self.iter_value.display)
        self.generate_btn.clicked.connect(self.__clicked_generate_mosaic__)

    @pyqtSlot()
    def __clicked_load__(self):
        img = QFileDialog.getOpenFileName(self)
        self.input_editor.setText(img[0])

    @pyqtSlot()
    def __err_value_changed__(self):
        rate = self.input_err_rate_slider.value() / self.input_err_rate_slider.maximum()
        self.input_err_rate.display(rate)

    @pyqtSlot()
    def __min_area_changed__(self):
        expon = self.input_min_area_slider.value()
        self.input_min_area.display(pow(4, expon))

    @pyqtSlot()
    def __clicked_generate_mosaic__(self):
        path = self.input_editor.text()
        if len(path) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Image path is empty")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif os.path.exists(path) is True:
            if platform.system() == 'Linux':    
                py = 'python3'
            else:
                py = 'python'
            err = self.input_err_rate.value()
            min_area = self.input_min_area.intValue()
            it = self.iter_value.intValue()
            is_plot_average = self.plot_average_radbtn.isChecked()
            is_plot_edge = self.plot_edge.isChecked()
            args = ""
            if is_plot_average is True:
                args += " -pa"
            else:
                args += " -pc"
            if is_plot_edge is True:
                args += " -pme"

            self.qth = ProgressThread(py, path, err, min_area, it, args, self)
            self.qth.start()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("File %s does not exist" %(path))
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    @pyqtSlot(int, name='progressUpdated')
    def __progress_updated__(self, value):
        self.progress.setValue(value)

    @pyqtSlot(bool)
    def __set_generated_btn__(self, value):
        self.generate_btn.setEnabled(value)

class ProgressThread(QThread):

    progress_trigger = pyqtSignal(int, name='progressUpdated')
    generate_btn_trigger = pyqtSignal(bool)

    def __init__(self, py, path, err, min_area, it, args, qobj):
        super().__init__()
        self.py = py
        self.path = path
        self.err = err
        self.min_area = min_area
        self.it = it
        self.args = args
        self.progress_trigger.connect(qobj.__progress_updated__)
        self.generate_btn_trigger.connect(qobj.__set_generated_btn__)

    def run(self):
        # Create temporary directory
        os.makedirs('.mosaic_tmp/')
        self.generate_btn_trigger.emit(False)
        self.progress_trigger.emit(1)

        os.system(
            "%s seedgen.py %s -e %f -ma %d -o .mosaic_tmp/seed.pickle" 
            %(self.py, self.path, self.err, self.min_area) 
        )

        self.progress_trigger.emit(34)

        os.system(
            "%s voronoigen.py -t %d -input %s -o %s" 
            %(self.py, self.it, '.mosaic_tmp/seed.pickle', '.mosaic_tmp/vordig.pickle') 
        )
        
        self.progress_trigger.emit(67)

        os.system(
            "%s mosaicplot.py %s -input %s" 
            %(self.py, self.args, '.mosaic_tmp/vordig.pickle') 
        )

        self.progress_trigger.emit(100)
        self.generate_btn_trigger.emit(True)
        # Remove temporary directory
        shutil.rmtree('.mosaic_tmp/')