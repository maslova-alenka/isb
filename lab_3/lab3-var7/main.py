import argparse

from asymmetric import Asymmetric
from symmetric import Symmetric
from working_with_a_file import read_json


def generation_action(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> None:
    asymmetric.generate_keys()
    asymmetric.serialization(setting["public_key"], setting["private_key"])
    symmetric.generate_key()
    symmetric.serialize_sym_key(setting["symmetric_key"])


def encryption_action(symmetric: Symmetric, setting: dict):
    symmetric.key_deserialization(setting["symmetric_key"])
    symmetric.encrypt(setting["initial_file"], setting["encrypted_file"])


def decryption_action(symmetric: Symmetric, setting: dict):
    symmetric.key_deserialization(setting["symmetric_key"])
    symmetric.decrypt(setting["encrypted_file"], setting["decrypted_file"])
    print("Create")


def menu():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true', help='Запускает режим дешифрования')

    args = parser.parse_args()
    setting = read_json("setting.json")
    symmetric = Symmetric()
    asymmetric = Asymmetric()
    match args:
        case args if args.generation:
            generation_action(symmetric, asymmetric, setting)
        case args if args.encryption:
            encryption_action(symmetric, setting)
        case args if args.decryption:
            decryption_action(symmetric, setting)
        case _:
            print("Необходимо указать один из флагов: --generation, --encryption or --decryption")


if __name__ == "__main__":
    menu()
