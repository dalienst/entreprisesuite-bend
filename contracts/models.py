from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from users.abstracts import UniversalIdModel, TimeStampedModel
from clients.models import Client
from payments.models import PaymentMethod

User = get_user_model()


class Contract(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    introduction = models.TextField()
    details = models.TextField()
    scope = models.TextField()
    services_provided = models.TextField()
    compensation_terms = models.TextField()
    termination_clause = models.TextField()
    legal_relationship = models.TextField()
    nda_clause = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("active", "Active"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    currency = models.CharField(max_length=15)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contract"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="contract_payment"
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Contract)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")
