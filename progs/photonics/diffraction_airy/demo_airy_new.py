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

from gui.simple_widget import SimpleWidget
from gui.title_widget import TitleWidget
from gui.open_widget import OpenFileWidget
from gui.graph_widget import GraphWidget
from gui.image_widget import ImageWidget
from gui.params_widget import ParamsWidget
from gui.slice_params_widget import SliceParamsWidget
from process.image_slice import ImageSlice
from process.airy import AiryDisc


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
        self.airy_simulation = AiryDisc()
        
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
        self.graph_area.set_x_label('Position in pixel')
        self.camera_area = SimpleWidget(title='Camera')
        self.params_area = ParamsWidget(title='Params')
        self.params_area.changed.connect(self.params_changed)

        # Central Menu
        self.slice_params = SliceParamsWidget(title='Menu')
        self.slice_params.changed.connect(self.params_changed)
        self.slice_params.set_graph_position_enabled(False)
        self.open_file_area = OpenFileWidget(title='Open File')
        self.open_file_area.opened.connect(self.init_image)

        # Include graphical elements in the window application
        self.main_layout.addWidget(self.title_area, 0, 0, 1, 3)
        self.main_layout.addWidget(self.slice_params, 1, 1)
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
        self.image_width = self.image.shape[1]
        self.image_height = self.image.shape[0]
        
        self.image_slice.set_image(self.image)
        self.slice_params.position.set_min_max_slider(1, self.image_height)
        
        self.image_area.set_image_from_array(self.image)
        max_v, max_ind = self.image_slice.find_max()
        self.slice_params.set_position(max_ind-1)
        delta_x = min(max_ind ,(self.image_height - max_ind))
        self.slice_params.set_mean_size_min_max(0, delta_x)
        self.slice_params.set_mean_size(0)
        self.slice_params.set_graph_position_min_max(-self.image_width//2, +self.image_width//2)
        self.slice_params.set_graph_position(0)
        
        
        
        self.refresh_image()
        self.refresh_graph()
    
    def refresh_image(self):
        try:
            max_ind, mean_size, g_pos = self.slice_params.get_data()
            # self.slice_params.set_mean_size(mean_size)
            self.image_area.draw_h_line(max_ind-1, width=5)
            self.image_area.draw_h_line(max_ind-1-mean_size)
            self.image_area.draw_h_line(max_ind-1+mean_size)
        except Exception as e:
            print("Exception - refresh_image: " + str(e) + "")
    
    def refresh_graph(self):
        y_list = []
        x_lin = np.linspace(0, self.image_width-1, self.image_width)
        max_ind, mean_size, g_pos = self.slice_params.get_data()
        self.image_slice.set_position(max_ind)
        self.image_slice.set_mean_size(mean_size)
        image_slice = self.image_slice.get_slice()
        y_list.append(image_slice)
        mean = self.image_slice.get_mean()
        x_axis_d = x_lin
        if mean.size != 0:
            y_list.append(mean)
        if self.simulation :
            dist, diam, wale, pixw = self.params_area.get_data()
            # X Axis
            self.maxIntensityInd = 0
            min_ax = (-(self.image_width)+self.maxIntensityInd-g_pos)/2*pixw*1e-6
            max_ax = ((self.image_width)+self.maxIntensityInd-g_pos)/2*pixw*1e-6
            x_axis = np.linspace(min_ax, max_ax, self.image_width)
            
            # Arbitrary intensity - To change
            simulated_disc = 255*self.airy_simulation.get_j(x_axis, diam, dist, wale)
            x_axis_d = x_axis*1e6 # Displayed axis
            y_list.append(simulated_disc)
            self.graph_area.set_x_label('Position in um')
        self.graph_area.set_data(x_axis_d, y_list)

    
    def params_changed(self, event):
        try:
            if event == 'params': # all the parameters are good
                self.simulation = True
                self.slice_params.set_graph_position_enabled(True)
            print(event)
            if event == 'slider:Position':
                max_ind, mean_size, g_pos = self.slice_params.get_data()
                delta_x = min(max_ind ,(self.image_height - max_ind))
                print(f'D_x = {delta_x}')
                self.slice_params.set_mean_size_min_max(0, delta_x-1)
                self.slice_params.set_mean_size(mean_size)
            self.refresh_image()
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
