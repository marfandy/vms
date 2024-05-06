import pytz
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from core.models import PurchaseOrder, PurchaseStatus
from core.utils import (
    calculate_average_response_time,
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
)


@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(sender, instance, created, update_fields=None, **kwargs):
    if update_fields:
        vendor = instance.fk_vendor

        if "status" in update_fields and instance.status == PurchaseStatus.completed:
            calculate_on_time_delivery_rate(vendor)

        if (
            "quality_rating" in update_fields
            and instance.status == PurchaseStatus.completed
        ):
            calculate_quality_rating_avg(vendor)

        if (
            "acknowledgment_date" in update_fields
            and instance.acknowledgment_date
            and instance.issue_date
        ):
            calculate_average_response_time(vendor)
