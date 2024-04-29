from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from .managers import AccountManager
from .utils import upload_to_profile_images


# Models
class Account(AbstractUser):
    PROFILE_IMAGE_ASPECT_RATIO = 1 / 1
    PROFILE_IMAGE_SIZE = (300, 300)
    PROFILE_IMAGE_THUMBNAIL_SIZE = (100, 100)

    # Choice classes
    class ThemeChoices(models.TextChoices):
        LIGHT = 'light', 'Light'
        DARK = 'dark', 'Dark'
        SYSTEM = 'system', 'System'

    email = models.EmailField(max_length=255, unique=True, verbose_name='Email', help_text='Unique email address')

    username = models.CharField(max_length=16, unique=True,
                                validators=[
                                    RegexValidator(regex='^[a-zA-Z0-9_]*$',
                                                   message='Username must be alphanumeric or contain any of the'
                                                           ' following: "_"',
                                                   code='invalid_username'),
                                    MinLengthValidator(limit_value=4,
                                                       message='Username must be at least 4 characters long')
                                ],
                                verbose_name='Username', help_text='Unique username associated with the account')

    name = models.CharField(max_length=120, blank=True, verbose_name='Name', help_text='Name of the user')

    description = models.TextField(max_length=300, blank=True, verbose_name='Description',
                                   help_text='User bio or description')

    profile_image = models.ImageField(upload_to=upload_to_profile_images, blank=True, null=True,
                                      verbose_name='Profile image',
                                      help_text='Profile image or avatar')

    theme = models.CharField(max_length=55, default=ThemeChoices.SYSTEM, choices=ThemeChoices.choices,
                             verbose_name='Theme', help_text='User website theme')

    email_verified = models.BooleanField(default=False, verbose_name='Email verified',
                                         help_text='Designates whether the user has verified their email address')

    is_marked_for_deletion = models.BooleanField(default=False, verbose_name='Is marked for deletion',
                                                 help_text='Designates whether the user has marked their account for\
                                                 deletion')

    date_marked_for_deletion = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                                    verbose_name='Date marked for deletion',
                                                    help_text='Server date and time when the user deleted their\
                                                    account')

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the account')

    short_uuid = models.CharField(max_length=8, unique=True, editable=False,
                                  validators=[
                                      MinLengthValidator(limit_value=8,
                                                         message='Short UUID must be exactly 8 characters long')
                                  ],
                                  verbose_name='Short UUID', help_text='Short unique identifier for the account'
                                  )

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date joined',
                                       help_text='Server date and time the account was created')

    last_login = models.DateTimeField(auto_now=True, verbose_name='Last login',
                                      help_text='Server date and time the account last logged in')

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = 'Accounts'
        verbose_name = 'Account'

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        # Set the date_deleted if the post is deleted
        if self.is_marked_for_deletion and self.date_marked_for_deletion is None:
            self.date_marked_for_deletion = timezone.now()

        # Call the original save method of models.model
        super().save(*args, **kwargs)

    @property
    def theme_choices_as_list(self):
        return [{'key': key, 'name': name} for i, (key, name) in enumerate(self.ThemeChoices.choices)]

    @staticmethod
    def get_theme_choices_as_dict():
        return dict(Account.ThemeChoices.choices)

    @staticmethod
    def get_theme_choices_as_list():
        """
        Returns the theme choices as a list of dictionaries with keys 'key' and 'name' for each choice.
        :return: list of dictionaries
        """
        return [{'key': key, 'name': name} for key, name in Account.ThemeChoices.choices]
