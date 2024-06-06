from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from users.abstracts import UniversalIdModel, TimeStampedModel
from milestones.models import Milestone

User = get_user_model()


class MilestoneTask(UniversalIdModel, TimeStampedModel):
    """
    A model to manage the tasks for specific milestones
    """

    name = models.CharField(max_length=1000)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("active", "Active"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    milestone = models.ForeignKey(
        Milestone, on_delete=models.CASCADE, related_name="milestone_tasks"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="milestone_tasks"
    )

    class Meta:
        verbose_name = "Milestone Task"
        verbose_name_plural = "Milestone Tasks"
        ordering = ["created_at"]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=MilestoneTask)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.name}-{instance.id}")
