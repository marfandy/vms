from datetime import timezone

from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from core.auth import isAuthenticated
from core.models import PurchaseOrder, PurchaseStatus, Vendors
from v1.serializers import (
    AcknowledgePurchaseOrderSerializer,
    PurchaseOrderCreateSerializer,
    PurchaseOrderListSerializer,
    PurchaseOrderUpdateSerializer,
    PurchaseQualityRatingSerializer,
    PurchaseStatusSerializer,
    VendorCreateSerializer,
    VendorListSerializer,
    VendorPerformanceSerializer,
    VendorUpdateSerializer,
)


class VendorsView(generics.ListAPIView):
    queryset = Vendors.objects.all()
    serializer_class = VendorCreateSerializer
    permission_classes = [isAuthenticated]

    @swagger_auto_schema(tags=["Vendors"])
    def get(self, request):
        try:
            data = self.get_queryset()
            serializer = VendorListSerializer(data, many=True)
            return Response(
                {
                    "data": serializer.data,
                    "message": "success",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Vendors"])
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "vandor created"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VendorDetailView(generics.ListAPIView):
    queryset = Vendors.objects.all()
    serializer_class = VendorUpdateSerializer
    permission_classes = [isAuthenticated]

    def get_object(self):
        try:
            return self.queryset.get(pk=self.kwargs["vendor_id"])
        except Vendors.DoesNotExist:
            return Response(
                {"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(tags=["Vendors"])
    def get(self, request, *args, **kwargs):
        data = self.get_object()
        try:
            serializer = VendorListSerializer(data, many=False)
            return Response(
                {"data": serializer.data, "message": "success"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(tags=["Vendors"])
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "vendor updated"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(tags=["Vendors"])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response(
                {"message": "vendor deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseOrderView(generics.ListAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderCreateSerializer
    permission_classes = [isAuthenticated]

    @swagger_auto_schema(tags=["Purchase Orders"])
    def get(self, request):
        try:
            data = self.get_queryset()
            serializer = PurchaseOrderListSerializer(data, many=True)
            return Response(
                {
                    "data": serializer.data,
                    "message": "success",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Purchase Orders"])
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
                return Response(
                    {"data": serializer.data, "message": "purchase order created"},
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseOrderDetailView(generics.ListAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderUpdateSerializer
    permission_classes = [isAuthenticated]

    def get_object(self):
        try:
            return self.queryset.get(pk=self.kwargs["po_id"])
        except Vendors.DoesNotExist:
            return Response(
                {"message": "Purchase order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(tags=["Purchase Orders"])
    def get(self, request, *args, **kwargs):
        data = self.get_object()
        try:
            serializer = PurchaseOrderListSerializer(data, many=False)
            return Response(
                {"data": serializer.data, "message": "success"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(tags=["Purchase Orders"])
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "purchase order updated"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(tags=["Purchase Orders"])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response(
                {"message": "purchase order deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VendorPerformanceView(generics.ListAPIView):
    queryset = Vendors.objects.all()
    serializer_class = VendorPerformanceSerializer
    permission_classes = [isAuthenticated]

    @swagger_auto_schema(tags=["Vendors"])
    def get(self, request, *args, **kwargs):
        try:
            data = Vendors.objects.get(id=kwargs["vendor_id"])
            serializer = self.get_serializer(data, many=False)
            return Response(
                {"data": serializer.data, "message": "success"},
                status=status.HTTP_200_OK,
            )
        except Vendors.DoesNotExist:
            return Response(
                {"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e), "code": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseOrderStatusView(generics.CreateAPIView):
    serializer_class = PurchaseStatusSerializer
    permission_classes = [isAuthenticated]

    @swagger_auto_schema(tags=["Purchase Orders"])
    def post(self, request, *args, **kwargs):
        try:
            _status = request.data.get("status")
            po = PurchaseOrder.objects.get(id=kwargs["po_id"])
            po.status = _status

            if _status == PurchaseStatus.completed:
                po.completed_date = timezone.now()

            po.save(update_fields=["status", "completed_date"])

            serializer = PurchaseOrderListSerializer(po, many=False)
            return Response(
                {"data": serializer.data, "message": "Status updated successfully"},
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"message": "Purchase order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PurchaseOrderRatingView(generics.CreateAPIView):
    serializer_class = PurchaseQualityRatingSerializer
    permission_classes = [isAuthenticated]

    @swagger_auto_schema(tags=["Purchase Orders"])
    def post(self, request, *args, **kwargs):
        try:
            _quality_rating = request.data.get("quality_rating")
            po = PurchaseOrder.objects.get(id=kwargs["po_id"])

            if po.status != PurchaseStatus.completed:
                return Response(
                    {"message": "Can't give rating for uncompleted order"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            po.quality_rating = _quality_rating

            po.save(update_fields=["quality_rating"])

            serializer = PurchaseOrderListSerializer(po, many=False)
            return Response(
                {
                    "data": serializer.data,
                    "message": "Quality rating updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"message": "Purchase order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class VendorAcknowledgePurchaseOrderView(generics.CreateAPIView):
    serializer_class = AcknowledgePurchaseOrderSerializer
    permission_classes = [isAuthenticated]

    @swagger_auto_schema(tags=["Purchase Orders"])
    def post(self, request, *args, **kwargs):
        try:
            _acknowledgment_date = request.data.get("acknowledgment_date")

            po = PurchaseOrder.objects.get(id=kwargs["po_id"])
            if po.issue_date == None:
                return Response(
                    {"message": "PO not issued to the vendor yet"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            po.acknowledgment_date = _acknowledgment_date
            po.save(update_fields=["acknowledgment_date"])

            return Response(
                {"message": "Acknowledgment updated successfully"},
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"message": "Purchase order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
