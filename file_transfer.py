import paramiko


class FileTransfer:
    """
    Jelenleg használaton kívül lévő, eleinte a fájlátvitel megvalósítására szolgáló osztály
    """
    def __init__(self, addr, usr, pw):
        """
        Az osztály konstruktora
        :param addr: Az átviteli célpont, azaz a Raspberry Pi IP-címe
        :param usr: A bejelentkezési felhasználónév
        :param pw: A bejelentkezéshez szükséges jelszó
        """
        self.ip = addr
        self.user = usr
        self.passwd = pw
        self.connect()

    def connect(self):
        """
        Ez a metódus az osztály server attribútumába eltárol egy SSH klienst, mellyel a konstruktorban paraméterként
        adott kiszolgálóhoz csatlakozik
        """
        self.server = paramiko.SSHClient()
        self.server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.server.connect(self.ip, username=self.user, password=self.passwd)
        # TODO ez itt valamiért errort dob
        self.sftp = self.server.open_sftp()
        print("Successfully connected to " + self.ip)

    def disconnect(self):
        """
        Az osztály server attribútumához tartozó SSH kliens bezárása
        """
        self.server.close()

    def upload(self, uploadable, to):
        """
        Fájl feltöltése az SSH kliensen keresztül
        :param uploadable: A feltölteni kívánt fájl
        :param to: Megadja, hogy a távoli szerveren hova szükséges feltölteni a fájlt
        """
        self.sftp.put(uploadable, to)
        print("Successful upload")
