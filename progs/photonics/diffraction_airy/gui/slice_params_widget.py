# -*- coding: utf-8 -*-
"""
SliceParamsWidget for LEnsE GUI Application

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
from gui.v_slider_widget import VSliderWidget


class SliceParamsWidget(QWidget):
    """
    SliceParamsWidget based on QWidget. 
    Parameters for slicing the original image
    
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
        self.position = VSliderWidget(name='Position', integer=True, inverted=True)
        self.position.slider.setMinimumHeight(300)
        self.position.set_units('px')
        self.position.changed.connect(self.params_changed)
        self.mean_size = VSliderWidget(name='Mean Size', integer=True)
        self.mean_size.slider.setMinimumHeight(100)
        self.mean_size.set_units('px')
        self.mean_size.changed.connect(self.params_changed)
        self.graph_position = VSliderWidget(name='Graph position', integer=True)
        self.graph_position.slider.setMinimumHeight(100)
        self.graph_position.set_min_max_slider(-100, 100)
        self.graph_position.set_units('')
        self.graph_position.changed.connect(self.params_changed)

        # Layout
        self.layout.addWidget(QLabel('Image (pixels)'), 0, 0) 
        self.layout.addWidget(self.position, 1, 0, 2, 1)  
        self.layout.addWidget(self.mean_size, 1, 1) 
        self.layout.addWidget(self.graph_position, 2, 1) 
    
    
    def get_data(self) -> (int, int, int):
        position = self.position.get_real_value()
        mean_size = self.mean_size.get_real_value()
        g_pos = self.graph_position.get_real_value()
        return position, mean_size, g_pos

    def set_position(self, value: int) -> None:
        self.position.set_value(value)

    def set_mean_size_min_max(self, min_v: int, max_v: int) -> None:
        self.mean_size.set_min_max_slider(min_v, max_v)
  
    def set_mean_size(self, value: int) -> None:
        self.mean_size.set_value(value)
        
    def set_graph_position_min_max(self, min_v, max_v) -> None:
        self.graph_position.set_min_max_slider(min_v, max_v)
        
    def set_graph_position(self, value: int) -> None:
        self.graph_position.set_value(value)
        
    def set_graph_position_enabled(self, value:bool) -> None:
        self.graph_position.setEnabled(value)
    
    def params_changed(self, event):
        try:
            self.changed.emit(event)
        except Exception as e:
            print("Exception - params_changed: " + str(e) + "")

   
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
