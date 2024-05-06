from django.db import models
from django.utils.translation import gettext_lazy as _

from core.behaviors import Timestampable


class PurchaseStatus(models.TextChoices):
    pending = "pending"
    completed = "completed"
    canceled = "canceled"


class Vendors(Timestampable, models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField(max_length=225)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        ordering = ["id"]
        db_table = "vendors"

    def __str__(self):
        return str(self.name)


class PurchaseOrder(Timestampable, models.Model):
    po_number = models.CharField(max_length=225, unique=True)
    fk_vendor = models.ForeignKey(
        Vendors,
        related_name="po_vendor",
        on_delete=models.CASCADE,
        verbose_name=_("Vendor"),
    )
    # ordering date to vendor
    order_date = models.DateTimeField(auto_now_add=True)
    # expected date item was delivered
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField(default=0)
    status = models.CharField(
        max_length=25, choices=PurchaseStatus.choices, default=PurchaseStatus.pending
    )
    issue_order = models.CharField(max_length=225, null=True)
    quality_rating = models.FloatField(null=True)
    # date when order sent to vendor
    issue_date = models.DateTimeField(null=True)
    # date vendor already received the order
    acknowledgment_date = models.DateTimeField(null=True)
    completed_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-id"]
        db_table = "purchase_orders"

    def __str__(self):
        return str(self.po_number)


class HistoricalPerformances(Timestampable, models.Model):
    fk_vendor = models.ForeignKey(
        Vendors,
        related_name="performance_vendor",
        on_delete=models.CASCADE,
        verbose_name=_("Vendor"),
    )
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        ordering = ["-id"]
        db_table = "historical_performances"

    def __str__(self):
        return str(self.fk_vendor.name)
