import paramiko


class FileTransfer:
    def __init__(self, addr, usr, pw):
        self.ip = addr
        self.user = usr
        self.passwd = pw
        self.connect()

    def connect(self):
        self.server = paramiko.SSHClient()
        self.server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.server.connect(self.ip, username=self.user, password=self.passwd)
        # TODO ez itt valamiért errort dob
        self.sftp = self.server.open_sftp()
        print("Successfully connected to " + self.ip)

    def disconnect(self):
        self.server.close()

    def upload(self, uploadable, to):
        self.sftp.put(uploadable, to)
        print("Successful upload")
