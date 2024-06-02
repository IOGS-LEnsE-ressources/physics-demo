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
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt6.QtGui import QIcon
import cv2
from scipy.special import j1

from gui.simple_widget import SimpleWidget
from gui.title_widget import TitleWidget
from gui.open_widget import OpenFileWidget
from gui.graph_widget import GraphWidget
from gui.image_widget import ImageWidget
from gui.params_widget import ParamsWidget
from process.image_slice import ImageSlice


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
        self.image_width = 0
        self.image_height = 0
        # If data from optical experiments are given, simulation of
        # Airy disc can be added
        self.simulation = False     
        
        self.image_slice = ImageSlice()
        
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
        self.main_layout.setRowStretch(2, 3) # Params
        
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        
        # Title Area
        self.title_area =  TitleWidget(title='Airy Disc / Demonstration')
        
        # Image Area
        self.image_area = ImageWidget(title='Image')
        self.graph_area = GraphWidget(title='Graphe')
        self.camera_area = SimpleWidget(title='Camera', 
                    background_color='gray',
                    text_color='black')
        self.params_area = ParamsWidget(title='Params')
        self.params_area.changed.connect(self.params_changed)

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
        self.image_width = self.image.shape[1]
        self.image_height = self.image.shape[0]
        
        self.image_slice.set_image(self.image)
        self.refresh_image()
        self.refresh_graph()
    
    def refresh_image(self):
        try:
            self.image_area.set_image_from_array(self.image)
            max_v, max_ind = self.image_slice.find_max()
            self.image_area.draw_h_line(max_ind)
        except Exception as e:
            print("Exception - refresh_image: " + str(e) + "")
    
    def refresh_graph(self):
        y_list = []
        x_lin = np.linspace(0, self.image_width-1, self.image_width)
        max_v, max_ind = self.image_slice.find_max()
        self.image_slice.set_position(max_ind)
        self.image_slice.set_mean_size(20)
        image_slice = self.image_slice.get_slice()
        y_list.append(image_slice)
        mean = self.image_slice.get_mean()
        if mean.size != 0:
            y_list.append(mean)
        if self.simulation :
            dist, diam, wale, pixw = self.params_area.get_data()
            # X Axis
            self.maxIntensityInd = 0
            self.origin = 0
            min_ax = (-(self.image_width)+self.maxIntensityInd+self.origin)/2*pixw*1e-6
            max_ax = ((self.image_width)+self.maxIntensityInd+self.origin)/2*pixw*1e-6
            x_axis = np.linspace(min_ax, max_ax, self.image_width)
            # Process Airy Disc calculation
            k = diam*1e-3/(dist*1e-2*wale*1e-9)
            J = (2*j1(np.pi*k*x_axis)/(np.pi*k*x_axis))**2
            # Arbitrary intensity - To change
            simulated_disc = 255*J
            y_list.append(simulated_disc)
            print('simu')
        self.graph_area.set_data(x_lin, y_list)
        
        
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
    
    def params_changed(self, event):
        try:
            if event == 'sliders':
                print('Slide test')
                if self.simulation:
                    print('Simu OK')
                self.refresh_graph()
                
            elif event == 'params': # all the parameters are good
                self.simulation = True
                self.refresh_graph()
        except Exception as e:
            print("Exception - params_changed: " + str(e) + "")

# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
