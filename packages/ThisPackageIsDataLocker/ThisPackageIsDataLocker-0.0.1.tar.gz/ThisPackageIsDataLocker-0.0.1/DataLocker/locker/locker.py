import os

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from DataLocker.utils.utils import read_file, write_file


class Locker:

    _salt = b'\xb5b}v=\xb4\xd8\xf0\x89Q\xbe\xa5S\x05\xbb\xc7\xbaw\\xcd\x1e\xc5.\x07\x0bI\x90\x02\x91\xe0\x95'


    def __init__(self, password):

        self._key = PBKDF2(password, Locker._salt, dkLen=32)
        self._mode = AES.MODE_CBC
        self._block_size = AES.block_size


    def _encrypt(self, data):

        cipher = self._init_encrypted_cipher()
        iv = cipher.iv
        cipher_data = cipher.encrypt(pad(data, self._block_size))

        return iv, cipher_data


    def _decrypt(self, cipher_data, iv):
        
        cipher = self._init_decrypted_cipher(iv)
        data = unpad(cipher.decrypt(cipher_data), self._block_size)

        return data


    def _add_lock_ext(self, file_path):

        lock_path = file_path + '.lock'
        os.rename(file_path, lock_path)


    def _remove_lock_path(self, file_path):

        base, _ = os.path.splitext(file_path)
        os.rename(file_path, base)


    def _init_encrypted_cipher(self):

        return AES.new(self._key, self._mode)


    def _init_decrypted_cipher(self, iv):

        return AES.new(self._key, self._mode, iv=iv)


    def lock(self, file_path):

        data = read_file(file_path)
        iv, cipher_data = self._encrypt(data)

        write_file(file_path, cipher_data, cipher_iv=iv)
        self._add_lock_ext(file_path)


    def unlock(self, file_path):

        iv, encrypted_data = read_file(file_path, block_size=self._block_size)
        decrypted_data = self._decrypt(encrypted_data, iv)

        write_file(file_path, decrypted_data)
        self._remove_lock_path(file_path)
