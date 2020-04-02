from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import re


class PublicKey(object):

    def __init__(self, key):
        self.raw_key = key
        self.format = None
        self.key_valid = False
        self.__preparation()

    def __preparation(self):
        self.rx_openssh = re.compile(r'ssh-rsa')
        self.rx_spki = re.compile(r'-----BEGIN PUBLIC KEY-----(?P<body>[a-zA-Z0-9\n\r/+]+)'
                                  r'-----END PUBLIC KEY-----', re.DOTALL | re.ASCII)
        self.rx_pkcs = re.compile(r'-----BEGIN RSA PUBLIC KEY-----(?P<body>[a-zA-Z0-9\n\r/+]+)'
                                  r'-----END RSA PUBLIC KEY-----', re.DOTALL | re.ASCII)
        if re.match(self.rx_openssh, self.raw_key):
            self.format = 'OpenSSH'
            self.load = serialization.load_ssh_public_key
        if a := re.match(self.rx_pkcs, self.raw_key):
            self.format = 'PKCS1'
            self.load = serialization.load_pem_public_key
            self.raw_key = f"-----BEGIN RSA PUBLIC KEY-----\n{a['body']}\n-----END RSA PUBLIC KEY-----"
        if a := re.match(self.rx_spki, self.raw_key):
            self.format = 'SubjectPublicKeyInfo'
            self.load = serialization.load_pem_public_key
            self.raw_key = f"-----BEGIN PUBLIC KEY-----\n{a['body']}\n-----END PUBLIC KEY-----"
        if not self.format:
            return
        try:
            self.__load_key()
            self.key_valid = True
        except ValueError:
            self.key_valid = False

    def __load_key(self):
        self.raw_key = self.raw_key.encode('ascii')
        self.key = self.load(data=self.raw_key, backend=default_backend())

    def convert_to_pkcs1(self, encoding):
        if not self.key_valid:
            return None
        format = serialization.PublicFormat.PKCS1
        if encoding == 'DER':
            encoding = serialization.Encoding.DER
            key = self.key.public_bytes(format=format, encoding=encoding)
            return key.hex()
        if encoding == 'PEM':
            encoding = serialization.Encoding.PEM
            key = self.key.public_bytes(format=format, encoding=encoding)
            return key.decode('ascii')

    def convert_to_openssh(self):
        if not self.key_valid:
            return None
        format = serialization.PublicFormat.OpenSSH
        encoding = serialization.Encoding.OpenSSH
        key = self.key.public_bytes(format=format, encoding=encoding)
        return key.decode('ascii')
