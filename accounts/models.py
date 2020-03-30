from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class UserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

def profile_pic_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/user_{0}/profile_pic/{1}'.format(instance.id, filename)


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='user name',
        max_length=127,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth   = models.DateField(null=True, blank=True)
    major           = models.CharField(max_length=64, null=True, blank=True)
    class_num       = models.CharField(max_length=64, null=True, blank=True)
    bio             = models.CharField(max_length=512, null=True, blank=True)
    profile_pic     = models.ImageField(upload_to=profile_pic_directory_path, null=True, blank=True)

    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'date_of_birth',]

    def __str__(self):
        return self.username + ' at ' + self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # resizing the uploaded profile picture 
    def save(self, *args, **kwargs):
        #Opening the uploaded image
        try:
            im = Image.open(self.profile_pic)

            output = BytesIO()

            #Resize/modify the image
            im = im.resize( (70,70) )

            #after modifications, save it to the output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            #change the imagefield value to be the newley modifed image value
            self.profile_pic = InMemoryUploadedFile(
                output,'ImageField', "%s.jpg" %self.profile_pic.name.split('.')[0],
                'image/jpeg', sys.getsizeof(output), None
            )

        except ValueError:
            pass

        super().save(*args, **kwargs)