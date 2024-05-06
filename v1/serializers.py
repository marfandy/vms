import pytz
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from core.models import PurchaseOrder, PurchaseStatus, Vendors


class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = [
            "id",
            "name",
            "contact_details",
            "address",
            "vendor_code",
            "created_at",
            "updated_at",
        ]


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = [
            "id",
            "name",
            "contact_details",
            "address",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
            "created_at",
            "updated_at",
        ]


class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ["name", "contact_details", "address", "vendor_code"]


class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ["name", "contact_details", "address", "vendor_code"]
        extra_kwargs = {
            "name": {"required": False},
            "contact_details": {"required": False},
            "address": {"required": False},
            "vendor_code": {"required": False},
        }


class PurchaseOrderListSerializer(serializers.ModelSerializer):
    fk_vendor = VendorListSerializer()

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "po_number",
            "fk_vendor",
            "order_date",
            "delivery_date",
            "items",
            "quantity",
            "status",
            "issue_order",
            "quality_rating",
            "issue_date",
            "acknowledgment_date",
            "completed_date",
            "created_at",
            "updated_at",
        ]


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "po_number",
            "fk_vendor",
            "delivery_date",
            "items",
            "quantity",
            "status",
        ]

        read_only_fields = ["id", "po_number", "status"]

    def create(self, validated_data):
        with transaction.atomic():
            prefix = "PO"
            now_utc = timezone.now()
            local_tz = pytz.timezone("Asia/Jakarta")
            local_dt = now_utc.astimezone(local_tz)
            last_number = (
                PurchaseOrder.objects.filter(
                    Q(created_at__year=local_dt.year, created_at__month=local_dt.month),
                    po_number__startswith=prefix,
                ).count()
                + 1
            )
            po_number = (
                f"{prefix}-{local_dt.year}{local_dt.month:02d}-{last_number:05d}"
            )
            validated_data["po_number"] = po_number
            instance = super().create(validated_data)
            return instance


class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "po_number",
            "fk_vendor",
            "delivery_date",
            "issue_order",
            "items",
            "quantity",
            "status",
            "issue_date",
        ]
        extra_kwargs = {
            "fk_vendor": {"required": False},
            "delivery_date": {"required": False},
            "items": {"required": False},
            "quantity": {"required": False},
            "issue_order": {"required": False},
        }
        read_only_fields = ["id", "po_number", "status"]


class AcknowledgePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["acknowledgment_date"]


class PurchaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["status"]


class PurchaseQualityRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ["quality_rating"]
