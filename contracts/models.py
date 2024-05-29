from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from users.abstracts import (
    UniversalIdModel,
    TimeStampedModel,
)
from clients.models import Client


User = get_user_model()


class ContractTemplate(UniversalIdModel, TimeStampedModel):
    """
    A template to differentiate different contract types
    """

    name = models.CharField(max_length=1000)
    introduction = models.TextField()
    details = models.TextField()
    service_provided = models.TextField()
    termination_policy = models.TextField()
    nda = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contract_templates"
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Contract Template"
        verbose_name_plural = "Contract Templates"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=ContractTemplate)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


class Contract(UniversalIdModel, TimeStampedModel):
    """
    Actual contract details
    - milestones
    - client details
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts")
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contract"
    )
    template = models.ForeignKey(
        ContractTemplate, on_delete=models.CASCADE, related_name="template_contracts"
    )
    project_scope = models.TextField()
    services_provided = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    legal_relationship = models.TextField()
    compensation_terms = models.TextField()
    termination_clause = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("active", "Active"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contract with {self.client.name}"


@receiver(pre_save, sender=Contract)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


class Milestone(UniversalIdModel, TimeStampedModel):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="milestones"
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    submission_deadline = models.DateField()
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} for {self.contract}"


@receiver(pre_save, sender=Milestone)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")


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

    def __str__(self):
        return self.name


@receiver(pre_save, sender=PaymentMethod)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")
