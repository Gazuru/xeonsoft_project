import requests


class ApiObject:
    """
    Az az osztály, mely lekérdezi a Raspberry Pi által futtatott REST API-tól a kiértékelés eredményeit
    """
    def __init__(self, ip_address):
        """
        Az osztály konstruktora
        :param ip_address: Az eszköz IP-címe, melyen az API szerver fut
        """
        self._address = ip_address
        self.response = None
        self._correct = 0.0
        self._faulty = 0.0

    def changed(self):
        """
        Ez a metódus az API válasz változásának függvényében változtatja a visszatérési értékét
        :return: True, hogyha változott a válasz
                 False, hogyha nem változott a válasz
        """
        if self.response == self.get_results():
            return False
        else:
            self.response = self.get_results()
            self._correct = float(self.response[0]['correct'])
            self._faulty = float(self.response[1]['faulty'])
            return True

    def get_results(self):
        """
        Ez a metódus lekérdezi az osztályhoz tartozó címről az API választ
        :return: A választ json formátumban, amennyiben létezik az objektum
        """
        response = requests.get("http://" + self._address + ":5000/results")
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def correct(self):
        """
        Ez a metódus dönti el, hogy a kiértékelés végeredményének mit tekintünk
        :return: True, ha jó a termék
                 False, ha hibás a termék
                 None, ha nincsen adat
        """
        if self._correct == 0.0 and self._faulty == 0.0:
            return None
        if self._correct > self._faulty:
            if self._correct > 0.6:
                return True
            else:
                return None
        else:
            return False


#
# A program belépési pontja
#
if __name__ == '__main__':
    a = ApiObject('192.168.1.67')
    while True:
        pass
