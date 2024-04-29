from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Asymmetric:
    """
    A class that implements asymmetric encryption and decryption using the RSA algorithm.

    Attributes
        private_key: The private key.
        public_key: The public key.
    """
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self) -> None:
        """
        Generates a new RSA private and public key pair.
        """
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.private_key = keys
        self.public_key = keys.public_key()

    def serialization(self, public_path: str, private_path: str) -> None:
        """
        Serializes the RSA public and private keys to files.

        Parameters
            public_path: The path to the file where the public key will be saved.
            private_path: The path to the file where the private key will be saved.
        """
        public_key = self.public_key
        private_key = self.private_key
        with open(public_path, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo))

        with open(private_path, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption()))

    def public_key_deserialization(self, public_path: str) -> None:
        """
        Deserializes the RSA public key from a file.

        Parameters
            public_path: The path to the file containing the public key.
        """
        with open(public_path, 'rb') as pem_in:
            public_bytes = pem_in.read()
        self.public_key = load_pem_public_key(public_bytes)

    def private_key_deserialization(self, private_path: str) -> None:
        """
        Deserializes the RSA private key from a file.

        Parameters
            private_path: The path to the file containing the private key.
        """
        with open(private_path, 'rb') as pem_in:
            private_bytes = pem_in.read()
        self.private_key = load_pem_private_key(private_bytes, password=None, )

    def encrypt(self, symmetric_key: bytes) -> bytes:
        """
        Encrypts a symmetric key using the public key.

        Parameters
            symmetric_key (bytes): The symmetric key to be encrypted.
        Returns
            The encrypted symmetric key.
        """
        encrypted_symmetric_key = self.public_key.encrypt(symmetric_key,
                                                          padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                       algorithm=hashes.SHA256(), label=None))
        return encrypted_symmetric_key

    def decrypt(self, symmetric_key: bytes) -> bytes:
        """
        Decrypts a symmetric key using the private key.

        Parameters
            symmetric_key (bytes): The encrypted symmetric key to be decrypted.
        Returns
            The decrypted symmetric key.
        """
        decrypted_symmetric_key = self.private_key.decrypt(symmetric_key,
                                                           padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                        algorithm=hashes.SHA256(), label=None))
        return decrypted_symmetric_key
