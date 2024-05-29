from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from users.abstracts import UniversalIdModel, TimeStampedModel
from clients.models import Client

User = get_user_model()


class PaymentMethod(UniversalIdModel, TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_methods"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_payment_method_name"
            )
        ]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=PaymentMethod)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


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
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contract"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="contract_payment"
    )

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
