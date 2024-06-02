# -*- coding: utf-8 -*-
"""
ImageSlice for Airy Disc demonstration
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

class ImageSlice:
    """
    ImageProcess class for processing images for Airy Disc demonstration
    """

    def __init__(self) -> None:
        """
        Initialisation of the class.
        """
        self.x_pos = 0      # position of the line to extract
        self.mean_size = 0  # number of lines to extract (*2 + 1)
        self.image = np.array([])   # image to process
    
    def set_image(self, image: np.ndarray) -> None:
        """
        Set an image to process
        """
        # Test if image in grayscale or not (number of element in shape)
        self.image = image
    
    def set_position(self, position: int) -> None:
        """
        Set the position of the line to extract
        """
        self.x_pos = position

    def set_mean_size(self, size: int) -> None:
        """
        Set the position of the line to extract
        """
        self.mean_size = size

    def get_slice(self) -> np.ndarray:
        """
        Return an array corresponding to the slice of the image at the x_pos
        """
        return self.image[self.x_pos, :]
       
    def get_mean(self) -> np.ndarray:
        """
        Return an array corresponding to the mean on X-axis
        """
        if self.mean_size == 0:
            return np.array([])
        else:
            return np.mean(self.image[self.x_pos-self.mean_size:self.x_pos+self.mean_size, :],axis=0)
        
    def find_max(self) -> (int, int):
        """ 
        Find Max intensity in gray image
        """
        self.maxIntensity = np.max(self.image)
        self.maxIntensityInd = np.argmax(self.image) // self.image.shape[1]
        return self.maxIntensity, self.maxIntensityInd
        
    
#--------------
# Example to test the Simple_Widget class

if __name__ == '__main__':
    im_proc = ImageSlice()
