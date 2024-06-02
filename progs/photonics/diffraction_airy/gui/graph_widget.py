# -*- coding: utf-8 -*-
"""
GraphWidget for LEnsE GUI Application

---------------------------------------
(c) 2024 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2024/06/02


Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on 02/jun/2024

@author: julien.villemejane
"""

import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from pyqtgraph import PlotWidget, plot, mkPen, PColorMeshItem

colors_list = [(128, 128, 0), (255, 0, 128), (128, 0, 255)]
pen_size_list = [3, 2, 2]

class GraphWidget(QWidget):
    """
    TitleWidget based on QWidget.
    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """

    def __init__(self, title='', background_color='#FFFFFF', text_color='#0A3250'):
        """
        Initialisation of the widget.
        """
        super().__init__(parent=None)
        self.title = title
        self.background_color = background_color
        self.text_color = text_color
        # Graph data
        self.x_axis = np.array([])
        self.y_axis = np.array([])
        self.y_size = 0
        
        # Style of the widget - based on CSS
        style_css = "color: "+self.text_color+"; font: bold 20px;"
        # style_css+= "background-color: "+self.background_color+";"
        # style_css+= "border-radius: 4px;"
        # style_css+= "border-color: black; border-width: 2px;"
        # style_css+= "border-style: solid;"
        self.setStyleSheet(style_css)

        # Create a self.layout and add widgets
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Graphical elements
        self.plot_area = PlotWidget()
        self.layout.addWidget(self.plot_area)
        self.plot_area.setBackground('w')
        self.plot_area.setYRange(0, 255, padding=0)
        # self.plot_area.setXRange(0, self.imageOrW-1, padding=0)
        self.plot_area.setLabel('bottom', 'Position in px')

        # row = 0
        self.layout.addWidget(self.plot_area, 0, 0) 

    def set_data(self, x_axis: np.ndarray, y_axis: list[np.ndarray]) -> None:
        '''
        '''
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x_size = len(self.x_axis)
        self.refresh_graph()

    def refresh_graph(self):
        """ Displaying data """
        self.plot_area.clear()
        self.plot_area.setXRange(self.x_axis[0], self.x_axis[self.x_size-1], padding=0)
        for i, y_values in enumerate(self.y_axis):
            pen = mkPen(color=colors_list[i], width=pen_size_list[i])
            self.plot_area.plot(self.x_axis, y_values, pen=pen)
    
    def set_x_label(self, label):
        """Update the label for X-Axis"""
        self.plot_area.setLabel('bottom', label)
        
#--------------
# Example to test the Simple_Widget class

if __name__ == '__main__':
    import sys
    from PyQt6.QtGui import QIcon

    class MyWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            # Define Window title
            self.setWindowTitle("LEnsE - Window Title")
            self.setWindowIcon(QIcon('images/IOGS-LEnsE-logo.jpg'))
            self.setGeometry(50, 50, 1000, 700)    
                    
            # Widget to test
            self.main_area = TitleWidget(title='Main Area', 
                        background_color='white',
                        text_color='red')
            self.setCentralWidget(self.main_area)
    
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())
