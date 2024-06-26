# -*- coding: utf-8 -*-
"""*widget_slider* file.

*widget_slider* file that contains :class::WidgetSlider 

.. module:: WidgetSlider
   :synopsis: class to display a slider in PyQt6.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

import sys

from PyQt6.QtWidgets import (
    QMainWindow,
    QGridLayout, QVBoxLayout,
    QWidget, QLineEdit, QLabel, QPushButton, QSlider,
    QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt


def is_number(value, min_val=0, max_val=0):
    """Return if the value is a valid number.
    
    Return true if the value is a number between min and max.

    :param value: Float number to test.
    :type value: float
    :param min_val: Minimum of the interval to test.
    :type min_val: float
    :param max_val: Maximum of the interval to test.
    :type max_val: float
    :return: True if the value is between min and max.
    :rtype: bool    

    """
    min_ok = False
    max_ok = False
    value2 = str(value).replace('.', '', 1)
    value2 = value2.replace('e', '', 1)
    value2 = value2.replace('-', '', 1)
    if value2.isdigit():
        value = float(value)
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        if (min_val != '') and (int(value) >= min_val):
            min_ok = True
        if (max_val != '') and (int(value) <= max_val):
            max_ok = True
        if min_ok != max_ok:
            return False
        else:
            return True
    else:
        return False


class SliderWidget(QWidget):
    """Create a Widget with a slider.
    
    SliderWidget class to create a widget with a slider and its value.
    Children of QWidget

    .. attribute:: name

        Name to display as the title.

        :type: str

    .. attribute:: ratio_slider

        Use to display non integer on the Slider.

        For example, with a ratio_slider at 10, the slider
        value of 500 corresponds to a real value of 50.0.

        :type: float

    .. attribute:: max_real_value

        Maximum value of the slider.

        :type: float

    .. attribute:: min_real_value

        Minimum value of the slider.

        :type: float

    .. attribute:: real_value

        Value of the slider.

        :type: float

    """

    changed = pyqtSignal(str)

    def __init__(self, name="", percent: bool = False,
                 integer: bool = False) -> None:
        """Default constructor of the class.
        
        :param name: Name of the slider, defaults to "".
        :type name: str, optional
        :param percent: Specify if the slider is in percent, defaults to False.
        :type percent: bool, optional
        :param integer: Specify if the slider is an integer, defaults to False.
        :type integer: bool, optional
        :param signal_name: Name of the signal, defaults to "".
        :type percent: str, optional

        """
        super().__init__(parent=None)

        # Global values
        self.percent = percent
        self.integer = integer
        self.min_real_value = 0
        self.max_real_value = 100
        self.ratio_slider = 10.0
        self.real_value = 1
        self.enabled = True
        self.name = name
        ''' Layout Manager '''
        self.main_layout = QGridLayout()
        ''' Graphical Objects '''
        self.name_label = QLabel(name)
        self.user_value = QLineEdit()
        self.real_value_label = QLabel('')
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(int(self.min_real_value * self.ratio_slider))
        self.slider.setMaximum(int(self.max_real_value * self.ratio_slider))
        self.slider.setValue(int(self.real_value * self.ratio_slider))
        self.units = ''
        self.units_label = QLabel('')

        # Adding graphical objects to the main layout 
        self.main_layout.addWidget(self.name_label, 0, 0)
        self.main_layout.addWidget(self.user_value, 0, 1)
        self.main_layout.addWidget(self.slider, 0, 2)
        self.main_layout.addWidget(self.real_value_label, 0, 3)
        self.main_layout.addWidget(self.units_label, 0, 4)
        self.main_layout.setColumnStretch(0, 1) 
        self.main_layout.setColumnStretch(1, 1) 
        self.main_layout.setColumnStretch(2, 3) 
        self.main_layout.setColumnStretch(3, 1) 
        self.main_layout.setColumnStretch(4, 1)
        self.setLayout(self.main_layout)

        for i in range(self.main_layout.rowCount()):
            self.main_layout.setRowStretch(i, 1)
        for i in range(self.main_layout.columnCount()):
            self.main_layout.setColumnStretch(i, 1)

        self.slider.valueChanged.connect(self.slider_changed)
        self.set_value(self.real_value)
        self.update_display()
        self.update_GUI()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.name_label.setText(name)

    def set_enabled(self, value):
        self.enabled = value
        self.update_GUI()
    
    def set_slider_enabled(self, value):
        self.slider.setEnabled(value)

    def update_GUI(self):
        self.slider.setEnabled(self.enabled)
        self.user_value.setEnabled(self.enabled)

    def is_value(self) -> bool:
        """
        """
        value = self.user_value.text()
        value2 = value.replace('.', '', 1)
        value2 = value2.replace('e', '', 1)
        value2 = value2.replace('-', '', 1)
        if value2.isdigit():
            return True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(f"Not a number")
            msg.setWindowTitle("Not a Number Value")
            msg.exec()
            self.real_value = self.min_real_value
            self.user_value.setText(str(self.real_value))
            return False        

    def update_value(self):
        if self.is_value():
            value = self.user_value.text()
            self.real_value = float(value)
            if self.integer:
                self.real_value = int(self.real_value)
            self.set_value(self.real_value)
        
        '''
        # Test if value is between min and max
        if not is_number(self.real_value, self.min_real_value, self.max_real_value):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText('This number is not in the good range')
            msg.setWindowTitle("Outside Range")
            msg.exec()
            self.real_value = self.min_real_value
            self.user_value.setText(str(self.real_value))
            self.real_value = self.min_real_value
        '''
        self.update_display()
        return True

    def slider_changed(self, event):
        self.real_value = self.slider.value() / self.ratio_slider
        if self.integer:
            self.real_value = int(self.real_value)
        self.real_value_label.setText(str(self.real_value))
        self.update_display()
        self.changed.emit('slider:' + self.name)

    def set_min_max_slider(self, min_val: float, max_val: float) -> None:
        """
        Set the minimum and maximum values of the slider.

        Parameters
        ----------
        min_val : float
            Minimum value of the slider.
        max_val : float
            Maximum value of the slider.

        """
        self.min_real_value = min_val
        self.max_real_value = max_val
        self.slider.setMinimum(int(self.min_real_value * self.ratio_slider))
        self.slider.setMaximum(int(self.max_real_value * self.ratio_slider))
        self.slider.setValue(int(self.min_real_value * self.ratio_slider))
        self.update_display()

    def set_units(self, units):
        self.units = units
        self.update_display()

    def update_display(self):
        display_value = self.real_value
        display_units = self.units
        if self.integer is False:
            if self.real_value / 1000 >= 1:
                display_value = display_value / 1000
                display_units = 'k' + self.units
            if self.real_value / 1e6 >= 1:
                display_value = display_value / 1e6
                display_units = 'M' + self.units
        self.real_value_label.setText(f'{display_value}')
        self.units_label.setText(f'{display_units}')

    def get_real_value(self):
        if self.integer:
            return int(self.slider.value() / self.ratio_slider)
        else:
            return self.slider.value() / self.ratio_slider
    
    def get_user_value(self):
        if self.integer:
            return int(float(self.user_value.text()))
        else:
            return float(self.user_value.text())

    def set_value(self, value):
        self.real_value = value
        self.user_value.setText(str(value))
        self.slider.setValue(int(self.real_value * self.ratio_slider))

    def set_ratio(self, value):
        self.ratio_slider = value
        self.slider.setMinimum(int(self.min_real_value * self.ratio_slider))
        self.slider.setMaximum(int(self.max_real_value * self.ratio_slider))
        self.slider.setValue(int(self.min_real_value * self.ratio_slider))
        self.update_display()


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication

    class MyWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Widget Slider test")
            self.setGeometry(300, 300, 200, 100)

            self.central_widget = QWidget()
            self.layout = QVBoxLayout()

            self.slider_widget = SliderWidget()
            self.slider_widget.set_min_max_slider(20, 50)
            self.slider_widget.set_units('Hz')
            self.slider_widget.set_name('Slider to test')
            self.layout.addWidget(self.slider_widget)

            self.central_widget.setLayout(self.layout)
            self.setCentralWidget(self.central_widget)


    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())
