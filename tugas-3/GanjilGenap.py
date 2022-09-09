class GanjilGenap(object):
    def __init__(self, angka_1, angka_2):
        self.angka_1 = angka_1
        self.angka_2 = angka_2

    def get_angka_1(self):
        return self.angka_1

    def get_angka_2(self):
        return self.angka_2

    def compare_angka(self):
        number_result = ""

        if(self.angka_1 == self.angka_2):
            number_result = str(self.angka_1) + \
                " sama dengan " + str(self.angka_2)
        elif(self.angka_1 > self.angka_2):
            number_result = str(self.angka_1) + \
                " lebih besar dari " + str(self.angka_2)
        else:
            number_result = str(self.angka_1) + \
                " lebih kecil dari " + str(self.angka_2)

        return number_result

    def is_odd(self, angka):
        number_result = ""

        if(int(angka) % 2 == 1):
            number_result = str(angka) + " adalah bilangan ganjil"
        else:
            number_result = str(angka) + " adalah bilangan genap"

        return number_result
