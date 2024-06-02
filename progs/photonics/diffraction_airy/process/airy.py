# -*- coding: utf-8 -*-
"""
AiryDisc for Airy Disc demonstration
LEnsE GUI Application

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
from scipy.special import j1


class AiryDisc:
    """
    AiryDisc class for processing simulation for Airy Disc demonstration
    """

    def __init__(self) -> None:
        """
        Initialisation of the class.
        """
        pass
    
    def get_j(self, x_axis, diameter, distance, wavelength) -> np.ndarray:
        """
        Return ...
        
        :param x_axis: Array of value where the function has to be evaluated
        :type x_axis: np.ndarray
        :param diameter: Diameter of the diffractive hole (mm)
        :type diameter: float
        :param distance: Distance between the diffractive hole and the sensor (cm)
        :type distance: float
        :param wavelength: Wavelenght of the signal (nm)
        :type wavelength: float
        :return: Array containing the evaluated value of the function.
        :rtype: np.ndarray
        """
        # Process Airy Disc calculation
        k = diameter*1e-3/(distance*1e-2*wavelength*1e-9)
        J = (2*j1(np.pi*k*x_axis)/(np.pi*k*x_axis))**2
        return J
#--------------
# Example to test the Simple_Widget class

if __name__ == '__main__':
    airy_simu = AiryDisc()
