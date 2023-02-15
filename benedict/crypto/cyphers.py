from Crypto import Random
from Crypto.Cipher import DES3

from benedict.serializers.base64 import Base64Serializer
from benedict.serializers.json import JSONSerializer


class AbstractCypher:
    """
    This class describes an abstract cypher.
    """

    def __init__(self):
        super().__init__()
        self._base64_serializer = Base64Serializer()
        self._json_serializer = JSONSerializer()

    def decrypt(self, s, encoding="utf-8", options=None):
        """
        Decrypt data:
        Base64 encrypted string -> decode Base64-> decrypt -> decode JSON -> data
        """
        encrypted_str = s
        encrypted_bytes = self._base64_serializer.decode(encrypted_str)
        cipher = self.get_cypher(options=options)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        decrypted_str = decrypted_bytes.decode(encoding)
        decrypted_str = decrypted_str.strip().strip("\x00").strip()
        decrypted_data = self._json_serializer.decode(decrypted_str)
        return decrypted_data

    def encrypt(self, data, block_size=0, encoding="utf-8", options=None):
        """
        Encrypt data:
        data -> encode JSON -> encrypt -> encode Base64 -> Base64 encrypted string
        """
        decrypted_data = data
        decrypted_str = self._json_serializer.encode(decrypted_data)
        if block_size:
            while len(decrypted_str) % block_size != 0:
                decrypted_str += " "
        decrypted_bytes = decrypted_str.encode(encoding)
        cypher = self.get_cypher(options=options)
        encrypted_bytes = cypher.encrypt(decrypted_bytes)
        encrypted_str = self._base64_serializer.encode(
            encrypted_bytes, encoding=encoding
        )
        return encrypted_str

    def get_cypher(self, options=None):
        raise NotImplementedError


class DES3Cypher(AbstractCypher):
    def __init__(self, key: str = "", mode=None):
        self._key = key or __name__
        self._mode = mode or DES3.MODE_ECB

    def get_cypher(self, options=None):
        options = options or {}
        key = options.get("key", self._key)
        mode = options.get("mode", self._mode)
        iv = Random.new().read(DES3.block_size)
        cipher = DES3.new(key, mode, iv)
        return cipher
