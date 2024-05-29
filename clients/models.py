from django.db import models
from django.contrib.auth import get_user_model

from users.abstracts import UniversalIdModel, TimeStampedModel

User = get_user_model()


class Client(UniversalIdModel, TimeStampedModel):
    """
    Adding personal clients
    Details about the clients
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
