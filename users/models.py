from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


from users.abstracts import (
    UniversalIdModel,
    AbstractProfileModel,
    TimeStampedModel,
)


class UserManager(BaseUserManager):
    """
    User manager for creating different users
    """

    use_in_migrations: bool = True

    def _create_user(self, username: str, email: str, password: str, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)

        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if not password:
            raise ValueError("Password is required")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if kwargs.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(username, email, password, **kwargs)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    UniversalIdModel,
    TimeStampedModel,
    AbstractProfileModel,
):
    """
    User model:
    - username
    - email
    - password
    - is_staff
    - is_active
    - is_verified
    - is_superuser
    - created_at
    - updated_at
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(
        unique=True,
    )
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    objects = UserManager()
    REQUIRED_FIELDS = ["username", "password"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self) -> str:
        return self.username
