from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        if not password:
            raise ValueError("User must have a password")
        email = self.normalize_email(email)
        user = self.model(email=email.lower(), **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    # gender = models.SmallIntegerField(choices=GENDER_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Document(models.Model):
    # docfile = models.FileField(upload_to='documents/% Y/% m/% d/')
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    @property
    def topic(self):
        ''' This methods returns first sentence as doc's topic '''
        try:
            words = self.text.split('.')[0]
            return words
        except:
            return None
    @property
    def vector(self):
        ''' This method returns the embedding of the document'''
        try:
            vect_ =  embed_model.get_text_embedding(self.text)
            return vect_
        except:
            return None

    def __str__(self):
        return f"{self.topic}: Date - [{self.uploaded_at.date()}]"
