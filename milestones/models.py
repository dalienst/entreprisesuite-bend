from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

from contracts.models import Contract
from users.abstracts import UniversalIdModel, TimeStampedModel

User = get_user_model()


class Milestone(UniversalIdModel, TimeStampedModel):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="milestones"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="milestone")
    name = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    submission_deadline = models.DateField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("active", "Active"),
            ("paid", "Paid"),
        ],
        default="pending",
    )
    file = CloudinaryField("milestone_file", blank=True, null=True)

    class Meta:
        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"
        ordering = ["created_at"]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Milestone)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")
