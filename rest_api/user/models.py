import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    """ Custom User Manager """

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        
        if not email:
            raise ValueError("User must have an email addres!")

        if re.findall('[0-9]+', first_name):
            raise ValueError(" User's name cannot contain numbers!")
        
        if re.findall('[0-9]+', last_name):
            raise ValueError(" User's name cannot contain numbers!")

        email = self.normalize_email(email=email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Overwritten model for the User in the system """
    
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """ Retrieve full name of user """
        return self.first_name + " " + self.last_name
    
    def get_short_name(self):
        """ Retrieve short name """
        return self.first_name

    def __str__(self) -> str:
        """ Return string representation of a user """
        return self.first_name