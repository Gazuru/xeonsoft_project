import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import pymongo


class Db:
    """
    Az adatbázis-kezelést megvalósító osztály
    """
    def __init__(self):
        """
        Az osztály konstruktora, melyben létrejön a kapcsolat
        """
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["xeonsoft_db"]
        self.collection = self.db["inference_results"]

    def insert(self, result_object):
        """
        Egy kiértékelési eredmény beszúrását megvalósító metódus
        :param result_object: az adatbázisba beszúrni kívánt kiértékelés eredménye
        """
        with open(result_object.img, "rb") as f:
            image = base64.b64encode(f.read())
            # print(result_object.img)
        result = {"image": image, "correct": result_object.correct, "faulty": result_object.faulty,
                  "uploaded": datetime.now()}
        self.collection.insert_one(result)

    def get(self):
        """
        A kép dekódolásának teszteléséhez felhasznált metódus
        """
        str = self.collection.find_one()["image"]
        im = Image.open(BytesIO(base64.b64decode(str)))
        im.save('test.png', 'PNG')


class Result:
    """
    A kiértékelés eredményét képviselő osztály
    """
    def __init__(self, correct=None, faulty=None, img=None):
        """
        Az osztály konstruktora
        :param correct: float, 0-tól 1-ig terjedő valószínűség, mely megadja mennyi eséllyel hibátlan a termék
        :param faulty: float, 0-tól 1-ig terjedő valószínűség, mely megadja mennyi eséllyel hibás a termék
        :param img: kép, amely alapján a kiértékelés történt
        """
        self._correct = correct
        self._faulty = faulty
        self._img = img

    @property
    def correct(self):
        """
        Property a '_correct' változó lekérdezésére
        :return: _correct
        """
        return self._correct

    @property
    def faulty(self):
        """
        Property a '_faulty' változó lekérdezésére
        :return: _faulty
        """
        return self._faulty

    @property
    def img(self):
        """
        Property az '_img' változó lekérdezésére
        :return: _img
        """
        return self._img

    @correct.setter
    def correct(self, value):
        """
        Setter a correct propertyhez
        :param value: A beállítani kívánt érték
        """
        self._correct = value

    @faulty.setter
    def faulty(self, value):
        """
        Setter a faulty propertyhez
        :param value: A beállítani kívánt érték
        """
        self._faulty = value

    @img.setter
    def img(self, value):
        """
        Setter az img propertyhez
        :param value: A beállítani kívánt érték
        """
        self._img = value


#
# A teszteléshez a program belépési pontja.
#
if __name__ == '__main__':
    db = Db()
    db.get()
