import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from working_with_a_file import read_bytes, write_bytes_text, write_file


class Symmetric:
    def __init__(self, key_path):
        self.key_path = key_path
        self.key = None

    def generate_key(self) -> None:
        self.key = os.urandom(16)

    def encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.SM4(self.key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, encrypted_path_text):
        text = read_bytes(encrypted_path_text)
        iv = text[:16]
        ciphertext = text[16:]
        cipher = Cipher(algorithms.SM4(self.key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        d_text = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.ANSIX923(32).unpadder()
        unpadded_dc_text = unpadder.update(d_text) + unpadder.finalize()
        d_text = unpadded_dc_text.decode('UTF-8')
        write_file(encrypted_path_text, d_text)
