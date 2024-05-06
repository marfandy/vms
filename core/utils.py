from datetime import timedelta

from django.db.models import Avg, F

from core.models import HistoricalPerformances, PurchaseOrder, PurchaseStatus, Vendors


def insert_to_history(data: dict):
    HistoricalPerformances.objects.create(**data)


def calculate_on_time_delivery_rate(vendor: Vendors):
    pos = PurchaseOrder.objects.filter(
        fk_vendor=vendor, status=PurchaseStatus.completed
    )
    completed_po = pos.count()  # count all pos

    on_time_deliverd = pos.filter(completed_date__lte=F("delivery_date")).count()

    on_time_delivery_rate = (
        (on_time_deliverd / completed_po) * 100 if completed_po > 0 else 0
    )
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

    insert_to_history(
        {
            "fk_vendor_id": vendor.id,
            "on_time_delivery_rate": on_time_delivery_rate,
        }
    )

    calculate_fulfillment_rate(vendor, pos)


def calculate_quality_rating_avg(vendor: Vendors):
    completed_po = PurchaseOrder.objects.filter(
        fk_vendor=vendor, status=PurchaseStatus.completed
    ).exclude(quality_rating=None)

    quality_rating_avg = (
        completed_po.aggregate(Avg("quality_rating"))["quality_rating__avg"] or 0
    )
    vendor.quality_rating_avg = quality_rating_avg
    vendor.save()

    insert_to_history(
        {
            "fk_vendor_id": vendor.id,
            "quality_rating_avg": quality_rating_avg,
        }
    )


def calculate_average_response_time(vendor: Vendors):
    complete_acknowledge_po = PurchaseOrder.objects.filter(
        fk_vendor=vendor, acknowledgment_date__isnull=False, issue_date__isnull=False
    )
    response_times = complete_acknowledge_po.annotate(
        response_time=Avg(F("acknowledgment_date") - F("issue_date"))
    ).aggregate(Avg("response_time"))["response_time__avg"] or timedelta(0)

    average_response_time = response_times.total_seconds() / 3600
    vendor.average_response_time = average_response_time
    vendor.save()
    insert_to_history(
        {
            "fk_vendor_id": vendor.id,
            "average_response_time": average_response_time,
        }
    )


def calculate_fulfillment_rate(vendor: Vendors, pos: PurchaseOrder):
    complete_pos = pos.count()

    pos_without_issue = pos.filter(issue_order__isnull=True).count()
    fulfillment_rate = (
        (pos_without_issue / complete_pos) * 100 if complete_pos > 0 else 0
    )
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
    insert_to_history(
        {
            "fk_vendor_id": vendor.id,
            "fulfillment_rate": fulfillment_rate,
        }
    )
