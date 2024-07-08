from django.db import models
import uuid
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

# Create your models here.

# Account Class to identify account
class Account (models.Model):
    # Fields to be saved in Account
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=240)
    username = models.CharField(max_length=240, unique=True)
    password = models.CharField(max_length=240)
    role = models.CharField(max_length=240)
    isDeactivated = models.BooleanField(default=False, null=False)
    email = models.EmailField(unique=True, null=False)
    registrationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# Gene
# Generate a key and salt for encryption (this should be securely stored and managed)
salt = os.urandom(16)
password = b'mysecretpassword'  # This should be managed securely
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

class GeneData(models.Model):
    geneID = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=100)
    encrypted_sequence = models.TextField()

    def __str__(self):
        return self.name

    def set_sequence(self, sequence):
        """Encrypt and store the sequence using AES."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(sequence.encode()) + padder.finalize()

        encrypted_sequence = encryptor.update(padded_data) + encryptor.finalize()
        self.encrypted_sequence = base64.b64encode(iv + encrypted_sequence).decode('utf-8')

    def get_sequence(self):
        """Decrypt and return the sequence using AES."""
        encrypted_data = base64.b64decode(self.encrypted_sequence.encode('utf-8'))
        iv = encrypted_data[:16]
        encrypted_sequence = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(encrypted_sequence) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        sequence = unpadder.update(padded_data) + unpadder.finalize()

        return sequence.decode('utf-8')

# No encryption
# class GeneData(models.Model):
#     geneID = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
#     name = models.CharField(max_length=100)
#     sequence = models.TextField()

#     def __str__(self):
#         return self.name
#     hello
# hehe


