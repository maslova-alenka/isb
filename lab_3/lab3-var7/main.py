import argparse

from asymmetric import Asymmetric
from symmetric import Symmetric
from working_with_a_file import read_json


def generation_action(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> None:
    symmetric.generate_key()
    asymmetric.generate_keys()
    asymmetric.serialization(setting["private_key"], setting["public_key"])


def encryption_action(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> dict:
    asymmetric.deserialization(setting["private_key"], setting["public_key"])
    return setting


def decryption_action(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> None:
    print(f"settings: {setting}")
    asymmetric.deserialization(setting["private_key"], setting["public_key"])


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
        generation_action(symmetric, asymmetric, setting)
    elif args.encryption is not None:
        setting = encryption_action(symmetric, asymmetric, setting)
    else:
        decryption_action(symmetric, asymmetric, setting)


if __name__ == "__main__":
    menu()
