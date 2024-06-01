# -*- coding: utf-8 -*-
"""
OpenFileWidget for LEnsE GUI Application

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
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os


class OpenFileWidget(QWidget):
    """
    OpenFileWidget based on QWidget.
    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """

    opened = pyqtSignal(str)

    def __init__(self, title='', background_color='#FFFFFF', text_color='#0A3250') -> None:
        """
        Initialisation of the widget.
        """
        super().__init__(parent=None)
        self.title = title
        self.background_color = background_color
        self.text_color = text_color
        self.file_name = ''
        self.real_file_name = ''
        
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
        self.layout.setRowStretch(0, 2) # Title
        self.layout.setRowStretch(1, 1) # Subtitle

        # Graphical elements
        self.title_label = QLabel('NO FILE')
        style_css = "color: "+self.text_color+";"
        self.title_label.setStyleSheet(style_css)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_bt = QPushButton('Select a file')
        style_css = "color: "+self.text_color+"; font: italic 14px;"
        self.file_bt.setStyleSheet(style_css)
        self.file_bt.clicked.connect(self.open_file_image)

        # row = 0
        self.layout.addWidget(self.title_label, 0, 0) 
        self.layout.addWidget(self.file_bt, 1, 0)  

    def open_file_image(self) -> None:
        self.open_file_name_dialog()
        '''
        self.initImage(self.fileName)
        self.refreshGraph()
        '''

    def open_file_name_dialog(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

        self.file_name, _ = file_dialog.getOpenFileName(self,
                        "QFileDialog.getOpenFileName()", "",
                        "Images (*.png *.jpg *.bmp)")
        if self.file_name:
            # file name with extension
            self.real_file_name = os.path.basename(self.file_name)
            self.opened.emit(self.file_name)
            self.title_label.setText(self.real_file_name)
            # self.openFileLabel.setText(os.path.splitext(self.realFileName)[0])

#--------------
# Example to test the Simple_Widget class

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow
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
