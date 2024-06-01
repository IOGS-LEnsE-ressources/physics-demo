# -*- coding: utf-8 -*-
"""Demo of Airy Disc

This GUI is developped in Python 3 and is based on 
PyQt6 for graphical objects.

---------------------------------------
(c) 2024 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2024/06/01


Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 01/jun/2024

@author: julien.villemejane
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt6.QtGui import QIcon
import cv2

from gui.simple_widget import SimpleWidget
from gui.title_widget import TitleWidget
from gui.open_widget import OpenFileWidget
from lensepy.pyqt6.widget_image_display import WidgetImageDisplay


# -------------------------------

class MainWindow(QMainWindow):
    """
    Our main window.

    Args:
        QMainWindow (class): QMainWindow can contain several widgets.
    """

    def __init__(self):
        """
        Initialisation of the main Window.
        """
        super().__init__()
        
        self.image_name = ''
        self.image = None
        
        # Define Window title
        self.setWindowTitle("LEnsE - Demo of Airy Disc")
        self.setGeometry(50, 50, 500, 400)
        # Main Widget
        self.main_widget = QWidget()

        # Main Layout
        self.main_layout = QGridLayout()
        # Left areas of size 2 / 5 of the width  
        self.main_layout.setColumnStretch(0, 2)
        self.main_layout.setColumnStretch(2, 2)
        # Central area of size 2 / 5 of the width
        self.main_layout.setColumnStretch(1, 1)
        # Row of size 1 / 2 of the height
        self.main_layout.setRowStretch(0, 1) # Title
        self.main_layout.setRowStretch(1, 10) # Main
        self.main_layout.setRowStretch(2, 5) # Params
        
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        
        # Title Area
        self.title_area =  TitleWidget(title='Airy Disc / Demonstration')
        
        # Image Area
        self.image_area = WidgetImageDisplay()
        self.graph_area = SimpleWidget(title='Graphe', 
                    background_color='gray',
                    text_color='white')
        self.camera_area = SimpleWidget(title='Camera', 
                    background_color='gray',
                    text_color='black')
        self.params_area = SimpleWidget(title='Params', 
                    background_color='lightgray',
                    text_color='black')

        # Central Menu
        self.main_menu = SimpleWidget(title='Menu')
        self.open_file_area = OpenFileWidget(title='Open File')
        self.open_file_area.opened.connect(self.init_image)

        # Include graphical elements in the window application
        self.main_layout.addWidget(self.title_area, 0, 0, 1, 3)
        self.main_layout.addWidget(self.main_menu, 1, 1)
        self.main_layout.addWidget(self.open_file_area, 2, 1)
        self.main_layout.addWidget(self.image_area, 1, 0)
        self.main_layout.addWidget(self.graph_area, 1, 2)
        self.main_layout.addWidget(self.camera_area, 2, 0)
        self.main_layout.addWidget(self.params_area, 2, 2)
        
        self.init_image('')

    def open_image(self, imageName):
        self.image = cv2.imread(imageName, cv2.IMREAD_GRAYSCALE)
        self.imageOrW = self.image.shape[1]     # width of the original image
        self.imageOrH = self.image.shape[0]     # height of the original image

    def init_image(self, event):
        if event != '':
            self.image_name = event
        """ Opening image """
        if self.image_name == '':
            self.open_image("./data/airy_1mm.bmp")
            print('Default Image')
        else:
            self.open_image(self.image_name)
            print(event)
        self.image_area.set_image_from_array(self.image)
        '''
        self.processRatio()
        """ Resizing image """
        self.resizeDispImage()
        """ Position Slider update """
        self.positionSlider.setMaximum(self.imageOrH) # depending on the height of the image
        self.positionSlider.setMinimum(1)
        
        """ Find Max intensity in gray image """
        self.maxIntensity = np.max(self.image)
        self.maxIntensityInd = np.argmax(self.image) // self.imageOrW 
        """ Set position of the slider to the maximum intensity line"""
        self.position = self.maxIntensityInd
        self.positionValue.setText(f'{self.position} px')
        self.positionSlider.setValue(self.maxIntensityInd)
        """ Mean Slider update """
        if((self.maxIntensityInd > self.maxMean) and (self.imageOrH-self.maxIntensityInd) > self.maxMean):
            self.meanSlider.setMaximum(self.maxMean)
        else:
            value = np.minimum(self.maxIntensityInd, self.imageOrH-self.maxIntensityInd)
            self.meanSlider.setMaximum(value)
        self.mean = int(self.meanSlider.value())
        self.meanValue.setText(f'{self.mean} px')
        
        """ Updating display of the image """
        self.updateImage()   
        '''

# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())