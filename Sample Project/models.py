from math import pi

class Lingkaran(object):
    def __init__(self):
        self.radius = 7
    def setRadius(self, r):
        self.radius = r
    def getRadius(self):
        return self.radius

    def hitungLuas(self):
        luas = pi * (self.radius ** 2)
        return luas

    def hitungKeliling(self):
        kel = 2 * pi * self.radius
        return kel

