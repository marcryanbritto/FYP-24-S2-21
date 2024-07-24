from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('doctor', 'Doctor'), ('patient', 'Patient')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Gene(models.Model):
    name = models.CharField(max_length=255)
    sequence = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genes')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sequence.startswith('ENC:'):
            self.sequence = self.encrypt_sequence(self.sequence)
        super(Gene, self).save(*args, **kwargs)

    def encrypt_sequence(self, sequence):
        if sequence.startswith('ENC:'):
            return sequence  # Already encrypted
        key = settings.SECRET_KEY[:32].encode()  # AES-256 key must be 32 bytes
        iv = os.urandom(16)  # AES block size is 16 bytes
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(sequence.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return 'ENC:' + base64.b64encode(iv + encrypted).decode()

    def decrypt_sequence(self):
        if not self.sequence.startswith('ENC:'):
            return self.sequence
        key = settings.SECRET_KEY[:32].encode()
        encrypted_data = base64.b64decode(self.sequence[4:].encode())
        iv = encrypted_data[:16]
        encrypted_sequence = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_sequence) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted.decode()

class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # e.g., 'login', 'logout', 'create_gene', etc.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
    
class Formula(models.Model):
    formula = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_formulas')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.formula
