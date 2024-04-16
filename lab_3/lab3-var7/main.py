import argparse

from asymmetric import Asymmetric
from symmetric import Symmetric
from working_with_a_file import read_json


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-gen', '--generation', help='Запускает режим генерации ключей')
group.add_argument('-enc', '--encryption', help='Запускает режим шифрования')
group.add_argument('-dec', '--decryption', help='Запускает режим дешифрования')

args = parser.parse_args()
setting = read_json("setting.json")
symmetric = Symmetric(setting["symmetric_key"])
asymmetric = Asymmetric(setting["public_key"], setting["private_key"])
if args.generation is not None:
    asymmetric.generate_keys()
elif args.encryption is not None:
    ciphertext = symmetric.encrypt(setting["initial_file"], setting["encrypted_file"])
else:
    plaintext = symmetric.decrypt(setting["encrypted_file"], setting["decrypted_file"])