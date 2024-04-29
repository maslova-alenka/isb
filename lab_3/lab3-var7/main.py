import argparse

from asymmetric import Asymmetric
from symmetric import Symmetric
from working_with_a_file import read_json, write_bytes_text, read_bytes


def generation_action(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> None:
    """
    Performs the key generation action.
    This function generates the asymmetric (public and private) keys and the symmetric key,
    and then serializes them to the specified files.

    Parameters
        symmetric: An instance of the Symmetric class.
        asymmetric: An instance of the Asymmetric class.
        setting: A dictionary containing the necessary settings, including the paths
                            for the public key, private key, and symmetric key files.
    """
    asymmetric.generate_keys()
    asymmetric.serialization(setting["public_key"], setting["private_key"])
    symmetric.generate_key()
    symmetric.serialize_sym_key(setting["symmetric_key"])


def encryption_action(symmetric: Symmetric, setting: dict) -> None:
    """
    Performs the encryption action using the symmetric key.

    Parameters:
        symmetric (Symmetric): An instance of the Symmetric class.
        setting (dict): A dictionary containing the necessary settings.
    """
    symmetric.key_deserialization(setting["symmetric_key"])
    symmetric.encrypt(setting["initial_file"], setting["encrypted_file"])


def decryption_action(symmetric: Symmetric, setting: dict):
    """
    Performs the decryption action using the symmetric key.

    Parameters
        symmetric: An instance of the Symmetric class.
        setting: A dictionary containing the necessary settings.
    """
    symmetric.key_deserialization(setting["symmetric_key"])
    symmetric.decrypt(setting["encrypted_file"], setting["decrypted_file"])


def encryption_symmetric_key(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> None:
    """
    Encrypts the symmetric key using the public key.

    Parameters
        symmetric: An instance of the Symmetric class.
        asymmetric: An instance of the Asymmetric class.
        setting: A dictionary containing the necessary settings.
    Returns
        The encrypted symmetric key.
    """
    symmetric.key_deserialization(setting["symmetric_key"])
    asymmetric.public_key_deserialization(setting["public_key"])
    symmetric_key = symmetric.key
    encrypted_symmetric_key = asymmetric.encrypt(symmetric_key)
    write_bytes_text(setting["encrypted_symmetric_key"], encrypted_symmetric_key)


def decryption_symmetric_key(symmetric: Symmetric, asymmetric: Asymmetric, setting: dict) -> bytes:
    """
    Decrypts the symmetric key using the private key.

    Parameters
        symmetric: An instance of the Symmetric class.
        asymmetric: An instance of the Asymmetric class.
        setting: A dictionary containing the necessary settings.
    Returns
        The decrypted symmetric key.
    """
    symmetric.key_deserialization(setting["symmetric_key"])
    asymmetric.private_key_deserialization(setting["private_key"])
    encrypted_symmetric_key = read_bytes(setting["encrypted_symmetric_key"])
    decrypted_symmetric_key = asymmetric.decrypt(encrypted_symmetric_key)
    symmetric.serialize_sym_key(setting["decrypted_symmetric_key"])
    return decrypted_symmetric_key


def menu():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Starts the key generation mode')
    group.add_argument('-enc', '--encryption', action='store_true', help='Starts the encryption mode')
    group.add_argument('-dec', '--decryption', action='store_true', help='Starts the decryption mode')
    group.add_argument('-enc_sym', '--encryption_symmetric', action='store_true',
                       help='Starts symmetric key encryption mode')
    group.add_argument('-dec_sym', '--decryption_symmetric', action='store_true',
                       help='Starts symmetric key encryption mode')

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
        case args if args.encryption_symmetric:
            encryption_symmetric_key(symmetric, asymmetric, setting)
        case args if args.decryption_symmetric:
            decryption_symmetric_key(symmetric, asymmetric, setting)
        case _:
            print("The wrong flag is selected")


if __name__ == "__main__":
    menu()
