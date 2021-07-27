import db_handler
import threading
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    """
    Csatlakozás esetén lefutó metódus
    A kliens feliratkozik a szükséges topicokra, ahonnan menti majd az érkező informáicót
    """
    if rc == 0:
        print("Connected to a broker!")
        client.subscribe("inference/img")
        client.subscribe("inference/correct")
        client.subscribe("inference/faulty")
    else:
        print("Hiba")


class Client:
    """
    Egy osztály, melynek egy objektuma pontosan egy MQTT subscribert valósít meg
    """
    def __init__(self, address, port=5000):
        """
        Az osztály konstruktora
        :param address: a broker címe
        :param port: a broker portja
        """
        mqtt.Client.connected_flag = False
        self._address = address
        self._port = port
        self._client = mqtt.Client("")
        self._client.on_connect = on_connect
        self._client.on_message = self.on_message
        self._result = db_handler.Result()
        self._db = db_handler.Db()
        threading.Thread(target=self.run, daemon=True).start()

    def on_message(self, client, userdata, message):
        """
        Eseménykezelő, amely akkor fut le, ha az egyik feliratkozott topic-ra üzenet érkezik
        """
        if "correct" in str(message._topic):
            self._result.correct = float(message.payload.decode())
        elif "faulty" in str(message._topic):
            self._result.faulty = float(message.payload.decode())
        else:
            with open(self._address + '.jpg', 'wb') as f:
                f.write(message.payload)
                self._result.img = f.name
                self._db.insert(self._result)

    def run(self):
        """
        A fő loop, melyet egy másik szál futtat. Amíg megy a fő alkalmazás, a kliens kapja az információt
        """
        self._client.connect(self._address, self._port)
        while True:
            self._client.loop_forever()

    @property
    def result(self):
        """
        Property, mellyel lekérdezhető az osztály '_result' attribútuma
        :return: _result
        """
        return self._result

#
# A program teszteléshez szükséges belépési pontja
#
if __name__ == '__main__':
    client = Client("192.168.1.67", 5000)
