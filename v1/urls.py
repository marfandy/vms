from unittest.mock import patch

from django.urls import path

from v1.views import (
    PurchaseOrderDetailView,
    PurchaseOrderRatingView,
    PurchaseOrderStatusView,
    PurchaseOrderView,
    VendorAcknowledgePurchaseOrderView,
    VendorDetailView,
    VendorPerformanceView,
    VendorsView,
)

app_name = "v1"

urlpatterns = [
    path("vendors/", VendorsView.as_view(), name="vendors"),
    path("vendors/<int:vendor_id>", VendorDetailView.as_view(), name="vendors_detail"),
    path(
        "vendors/<int:vendor_id>/performance",
        VendorPerformanceView.as_view(),
        name="vendors_performance",
    ),
    path("purchase_orders/", PurchaseOrderView.as_view(), name="po"),
    path(
        "purchase_orders/<int:po_id>",
        PurchaseOrderDetailView.as_view(),
        name="po_detail",
    ),
    path(
        "purchase_orders/<int:po_id>/status",
        PurchaseOrderStatusView.as_view(),
        name="po_status",
    ),
    path(
        "purchase_orders/<int:po_id>/rating",
        PurchaseOrderRatingView.as_view(),
        name="po_rating",
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge",
        VendorAcknowledgePurchaseOrderView.as_view(),
        name="po_acknowledge",
    ),
]
