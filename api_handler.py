import requests


class ApiObject:
    def __init__(self, ip_address):
        self._address = ip_address
        self.response = None
        self._correct = 0.0
        self._faulty = 0.0

    def changed(self):
        if self.response == self.get_results():
            return False
        else:
            self.response = self.get_results()
            self._correct = float(self.response[0]['correct'])
            self._faulty = float(self.response[1]['faulty'])
            return True

    def get_results(self):
        response = requests.get("http://" + self._address + ":5000/results")
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def correct(self):
        if self._correct == 0.0 and self._faulty == 0.0:
            return None
        if self._correct > self._faulty:
            if self._correct > 0.6:
                return True
            else:
                return None
        else:
            return False


if __name__ == '__main__':
    a = ApiObject('192.168.1.67')
    while True:
        pass
