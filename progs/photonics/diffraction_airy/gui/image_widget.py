# -*- coding: utf-8 -*-
"""
ImageWidget for LEnsE GUI Application

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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from lensepy.pyqt6.widget_image_display import WidgetImageDisplay



class ImageWidget(WidgetImageDisplay):
    """
    TitleWidget based on WidgetImageDisplay.
    Args:
        WidgetImageDisplay (class): QWidget can be put in another widget and / or window.
    """

    def __init__(self, title='', background_color='#FFFFFF', text_color='#0A3250'):
        """
        Initialisation of the widget.
        """
        super().__init__()
        self.title = title
        self.background_color = background_color
        self.text_color = text_color
        
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
