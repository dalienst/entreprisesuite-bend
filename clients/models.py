from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

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
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Client)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")
