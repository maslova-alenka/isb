import argparse

from asymmetric import Asymmetric
from symmetric import Symmetric
from working_with_a_file import read_json


def generation_action(symmetric: Symmetric, asymmetric: Asymmetric, settings: dict) -> None:
    symmetric.generate_key()
    asymmetric.generate_keys()
    symmetric.sym = asymmetric.encrypt(symmetric.sym)
    asymmetric.serialization(settings["private_key"], settings["public_Key"])


def menu():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', help='Запускает режим дешифрования')

    args = parser.parse_args()
    setting = read_json("setting.json")
    symmetric = Symmetric()
    asymmetric = Asymmetric()
    if args.generation is not None:
        asymmetric.generate_keys()
    elif args.encryption is not None:
        ciphertext = symmetric.encrypt(setting["initial_file"], setting["encrypted_file"])
    else:
        plaintext = symmetric.decrypt(setting["encrypted_file"], setting["decrypted_file"])