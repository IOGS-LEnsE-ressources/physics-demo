# -*- coding: utf-8 -*-
"""
ParamsWidget for LEnsE GUI Application

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


# Graphical interface
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from gui.slider_widget import SliderWidget


class ParamsWidget(QWidget):
    """
    ParamsWidget based on QWidget. 
    Allow to add experimental data for simulating Airy Disc.
    
    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """
    
    changed = pyqtSignal(str)

    def __init__(self, title=''):
        """
        Initialisation of the widget.
        """
        super().__init__(parent=None)
        self.title = title
        self.text_color = '#0A3250'
        
        # Style of the widget - based on CSS
        style_css = "color: "+self.text_color+"; font: 12px;"
        self.setStyleSheet(style_css)

        # Create a self.layout and add widgets
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Graphical elements
        self.distance = SliderWidget(name='Distance')
        self.distance.set_units('cm')
        self.distance.set_slider_enabled(False)
        self.distance.changed.connect(self.params_changed)
        self.diameter = SliderWidget(name='Diameter')
        self.diameter.set_units('mm')
        self.diameter.set_ratio(50)
        self.diameter.set_slider_enabled(False)
        self.diameter.changed.connect(self.params_changed)
        self.wavelength = SliderWidget(name='Wavelength')
        self.wavelength.set_units('nm')
        self.wavelength.set_slider_enabled(False)
        self.wavelength.changed.connect(self.params_changed)

        # Layout
        self.layout.addWidget(self.distance, 0, 0) 
        self.layout.addWidget(self.diameter, 1, 0) 
        self.layout.addWidget(self.wavelength, 2, 0) 
        
        # Update and Camera Pixel Widget
        self.pixels_size = SliderWidget(name='Pixels Size')
        self.pixels_size.set_units('um')
        self.pixels_size.set_ratio(50)
        self.pixels_size.set_slider_enabled(False)
        self.pixels_size.changed.connect(self.params_changed)
        self.update_widget = QWidget()
        self.update_layout = QGridLayout()
        self.update_widget.setLayout(self.update_layout)
        
        self.update_bt = QPushButton('Update Data')
        self.update_bt.clicked.connect(self.data_updated)
        self.update_layout.addWidget(self.pixels_size, 0, 0)
        self.update_layout.addWidget(self.update_bt, 0, 1)
        
        self.layout.addWidget(self.update_widget, 3, 0) 
    
    
    def get_data(self):
        dist = self.distance.get_real_value()
        diam = self.diameter.get_real_value()
        wale = self.wavelength.get_real_value()
        pixw = self.pixels_size.get_real_value()
        return dist, diam, wale, pixw
    
    
    def params_changed(self, event):
        try:
            self.changed.emit('sliders')
        except Exception as e:
            print("Exception - params_changed: " + str(e) + "")

    
    def data_updated(self, event):
        params_count = 0
        try:
            if self.distance.update_value():
                params_count += 1
                distance = self.distance.get_real_value()
                self.distance.set_min_max_slider(distance*0.9, distance*1.1)
                self.distance.set_value(distance)
                self.distance.set_slider_enabled(True)
            if self.diameter.update_value():
                params_count += 1
                diameter = self.diameter.get_real_value()
                self.diameter.set_min_max_slider(diameter*0.9, diameter*1.1)
                self.diameter.set_value(diameter)
                self.diameter.set_slider_enabled(True) 
            if self.wavelength.update_value():
                params_count += 1
                wavelength = self.wavelength.get_real_value()
                self.wavelength.set_min_max_slider(wavelength*0.9, wavelength*1.1)
                self.wavelength.set_value(wavelength)
                self.wavelength.set_slider_enabled(True)
            if self.pixels_size.update_value():
                params_count += 1
                pixels_size = self.pixels_size.get_real_value()
                self.pixels_size.set_min_max_slider(pixels_size*0.9, pixels_size*1.1)
                self.pixels_size.set_value(pixels_size)
                self.pixels_size.set_slider_enabled(True)
            if params_count == 4:
                self.changed.emit('params')
        except Exception as e:
            print("Exception - data_updated: " + str(e) + "")
    
   
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
            self.main_area = ParamsWidget(title='Main Area', 
                        background_color='white',
                        text_color='red')
            self.setCentralWidget(self.main_area)
    
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())
