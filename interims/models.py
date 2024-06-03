from django.db import models
from django.contrib.auth import get_user_model

from users.abstracts import UniversalIdModel, TimeStampedModel
from milestones.models import Milestone

User = get_user_model()

# class InterimInvoice(UniversalIdModel, TimeStampedModel):
#     """
#     An invoice to be sent out to request payment for completed milestones
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interim_invoices")
#     milestone = models