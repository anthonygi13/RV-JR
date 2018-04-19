# Authors: Giraudo Anthony, Kari Hichma, Marinho Louise, Kilian Mac Donald
# 19 février 2018
# conversions.py

from math import pi


def radian(angle):
    """
    :param angle: angle en degres a convertir en radians
    :return: angle correspondant en radians
    """
    return (angle / 360) * 2 * pi

def metre(pixels):
    """
    :param pixels: nombre de pixels a convertir
    :return: conversion des pixels en m (echelle de 15 cm pour 100 pixels)
    """
    return pixels / 100 * 0.15

def pixel(metres):
    """
    :param metres: nombre de metres a convertir
    :return: conversions des metres en pixels (echelle de 15 cm pour 100 pixels)
    """
    return metres / 0.15 * 100

