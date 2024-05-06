import argparse
import json

from asymmetric import Asymmetric
from symmetric import Symmetric
from working_with_a_file import write_bytes_text, read_bytes


def read_settings(settings_file):
    try:
        with open(settings_file, "r") as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        print(f"Settings file '{settings_file}' not found.")
    except Exception as e:
        print(f"Error reading settings file: {str(e)}")


def write_settings(settings_file, settings):
    try:
        with open(settings_file, "w") as file:
            json.dump(settings, file)
    except Exception as e:
        print(f"Error writing settings file: {str(e)}")


def generation_action(symmetric: Symmetric, asymmetric: Asymmetric,
                      path_public: str, path_private: str, path_symmetric: str) -> None:
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
    asymmetric.serialization_public(path_public)
    asymmetric.serialization_private(path_private)
    symmetric.generate_key()
    symmetric.serialize_sym_key(path_symmetric)


def encryption_action(symmetric: Symmetric, path_symmetric: str, path_initial: str, path_encrypted: str) -> None:
    """
    Performs the encryption action using the symmetric key.

    Parameters:
        symmetric: An instance of the Symmetric class.
        path_symmetric: Path to the symmetric key file.
        path_initial: Path to the initial file to be encrypted.
        path_encrypted: Path to the encrypted file.
    """
    symmetric.key_deserialization(path_symmetric)
    symmetric.encrypt(path_initial, path_encrypted)


def decryption_action(symmetric: Symmetric, path_symmetric: str, path_encrypted: str, path_decrypted: str) -> None:
    """
    Performs the decryption action using the symmetric key.

    Parameters
        symmetric: An instance of the Symmetric class.
        path_symmetric: Path to the symmetric key file.
        path_encrypted: Path to the encrypted file.
        path_decrypted: Path to the decrypted file.
    """
    symmetric.key_deserialization(path_symmetric)
    symmetric.decrypt(path_encrypted, path_decrypted)


def encryption_symmetric_key(symmetric: Symmetric, asymmetric: Asymmetric,
                             path_symmetric: str, path_public: str, path_enc_sym_key: str) -> None:
    """
    Encrypts the symmetric key using the public key.

    Parameters
        symmetric: An instance of the Symmetric class.
        asymmetric: An instance of the Asymmetric class.
        path_symmetric: Path to the symmetric key file.
        path_public: Path to the public key file.
        path_enc_sym_key: Path to the encrypted symmetric key file.
    Returns
        The encrypted symmetric key.
    """
    symmetric.key_deserialization(path_symmetric)
    asymmetric.public_key_deserialization(path_public)
    symmetric_key = symmetric.key
    encrypted_symmetric_key = asymmetric.encrypt(symmetric_key)
    write_bytes_text(path_enc_sym_key, encrypted_symmetric_key)


def decryption_symmetric_key(symmetric: Symmetric, asymmetric: Asymmetric,
                             path_symmetric: str, path_private: str, path_enc_sym_key: str,
                             path_dec_sym_key: str) -> bytes:
    """
    Decrypts the symmetric key using the private key.

    Parameters
        symmetric: An instance of the Symmetric class.
        asymmetric: An instance of the Asymmetric class.
        path_symmetric: Path to the symmetric key file.
        path_private: Path to the private key file.
        path_enc_sym_key: Path to the encrypted symmetric key file.
        path_dec_sym_key: Path to the decrypted symmetric key file.
    Returns
        The decrypted symmetric key.
    """
    symmetric.key_deserialization(path_symmetric)
    asymmetric.private_key_deserialization(path_private)
    encrypted_symmetric_key = read_bytes(path_enc_sym_key)
    decrypted_symmetric_key = asymmetric.decrypt(encrypted_symmetric_key)
    symmetric.serialize_sym_key(path_dec_sym_key)
    return decrypted_symmetric_key


def menu():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Starts the key generation mode')
    group.add_argument('-enc', '--encryption', help='Starts the encryption mode')
    group.add_argument('-dec', '--decryption', help='Starts the decryption mode')
    group.add_argument('-enc_sym', '--encryption_symmetric', help='Starts symmetric key encryption mode')
    group.add_argument('-dec_sym', '--decryption_symmetric', help='Starts symmetric key encryption mode')

    args = parser.parse_args()
    setting = read_settings("setting.json")
    symmetric = Symmetric()
    asymmetric = Asymmetric()
    match args:
        case args if args.generation:
            generation_action(symmetric, asymmetric, setting["public_key"], setting["private_key"],
                              setting["symmetric_key"])
        case args if args.encryption:
            encryption_action(symmetric, setting["symmetric_key"], setting["initial_file"], setting["encrypted_file"])
        case args if args.decryption:
            decryption_action(symmetric,setting["symmetric_key"], setting["encrypted_file"], setting["decrypted_file"])
        case args if args.encryption_symmetric:
            encryption_symmetric_key(symmetric, asymmetric, setting["symmetric_key"], setting["public_key"],
                                     setting["encrypted_symmetric_key"])
        case args if args.decryption_symmetric:
            decryption_symmetric_key(symmetric, asymmetric, setting["symmetric_key"], setting["private_key"],
                                     setting["encrypted_symmetric_key"], setting["decrypted_symmetric_key"])
        case _:
            print("The wrong flag is selected")


if __name__ == "__main__":
    menu()
