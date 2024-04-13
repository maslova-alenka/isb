from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Asymmetric:
    def __init__(self, public_key_path, private_key_path):
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path
        self.private_key = None
        self.public_key = None

    def generate_keys(self) -> None:
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.private_key = keys
        self.public_key = keys.public_key()

    def serialization(self) -> None:
        public_key = self.public_key_path
        private_key = self.private_key_path
        with open(public_key, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo))

        with open(private_key, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption()))

    def deserialization(self):
        public_key = self.public_key_path
        private_key = self.private_key_path
        with open(public_key, 'rb') as pem_in:
            public_bytes = pem_in.read()
        self.public_key = load_pem_public_key(public_bytes)

        with open(private_key, 'rb') as pem_in:
            private_bytes = pem_in.read()
        self.private_key = load_pem_private_key(private_bytes, password=None, )

    def encrypt(self, symmetric_key: bytes) -> bytes:
        encrypted_symmetric_key = self.private_key.encrypt(symmetric_key,
                                                           padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                        algorithm=hashes.SHA256(), label=None))
        return encrypted_symmetric_key

    def decrypt(self, symmetric_key: bytes) -> bytes:
        decrypted_symmetric_key = self.private_key.decrypt(symmetric_key,
                                                           padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                        algorithm=hashes.SHA256(), label=None))
        return decrypted_symmetric_key
