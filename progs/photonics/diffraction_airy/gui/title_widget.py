# -*- coding: utf-8 -*-
"""
TitleWidget for LEnsE GUI Application

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


class TitleWidget(QWidget):
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
        self.layout.setColumnStretch(0, 7)
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(0, 2) # Title
        self.layout.setRowStretch(1, 1) # Subtitle

        # Graphical elements
        self.title_label = QLabel(self.title)
        style_css = "color: "+self.text_color+";"
        self.title_label.setStyleSheet(style_css)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label = QLabel('Developed by the LEnsE')
        style_css = "color: "+self.text_color+"; font: italic 14px;"
        self.subtitle_label.setStyleSheet(style_css)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # row = 0
        self.layout.addWidget(self.title_label, 0, 0) 
        self.layout.addWidget(self.subtitle_label, 1, 0) 
        
        # Logo LEnsE
        self.lense_logo = QLabel()
        imageSize = self.lense_logo.size()
        logo = QPixmap("./data/IOGS-LEnsE-logo_small.jpg")
        # logo = logo.scaled(imageSize.width(), imageSize.height(), Qt.AspectRatioMode.KeepAspectRatio)
        self.lense_logo.setPixmap(logo)
        self.lense_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addWidget(self.lense_logo, 0, 1, 2, 1) 
        
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
