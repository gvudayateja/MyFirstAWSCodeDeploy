from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

POSITION = (
    (u'NEW', u'NEW'),
    (u'JUNIOR', u'JUNIOR'),
    (u'SENIOR', u'SENIOR'),
    (u'PROFESSIONAL', u'PROFESSIONAL'),
)


class Author(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    exp = models.CharField(choices=POSITION, max_length=255)

    def __str__(self):
        return self.firstname


class Category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    category = models.ForeignKey(Category)
    description = RichTextField()
    posted = models.DateField(default=timezone.now)
    photo = RichTextUploadingField()

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.CharField(max_length=255)
    file = models.FileField("File", upload_to='files/', default='', blank=True)
    pic = models.ImageField("Image", upload_to='images/', default='', blank=True)


class User(AbstractUser):
    mobile = models.CharField(max_length=10)
    pin = models.CharField(max_length=4)

    objects = UserManager()

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    subscriber_name = models.CharField(max_length=64)
    subscriber_email = models.EmailField()
    subscribed_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.subscriber_name
