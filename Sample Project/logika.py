class Logika(object):
    def __init__(self):
        self.a = 0
        self.b = 5
    
    def setA(self, a):
        self.a = a
    def setB(self, b):
        self.b = b
    def logikaif(self):
        a = self.a
        b = self.b
        if(a>b):
            hasil = "A Lebih Besar dari B"
        elif(a==b):
            hasil = "A sama dengan B"
        else:
            hasil = "A Lebih kecil dari B"
        return hasil


