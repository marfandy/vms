from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import PurchaseOrder, PurchaseStatus, Vendors

now = datetime.now()


class BaseTest(APITestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "admin!@#"
        self.token = self.get_token()
        self.vendor_id = self.get_vendor()
        delivery_date = now + timedelta(days=10)
        self.delivery_date_str = delivery_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.po_id = self.get_purchase_order()

    def get_token(self):
        response = self.client.post(
            reverse("authentication:signin"),
            {"username": self.username, "password": self.password},
        )
        return response.data["token"]["access"]

    def get_vendor(self):
        return Vendors.objects.create(
            name="Vendor A",
            contact_details="Contact",
            address="Address",
            vendor_code="A123",
        ).id

    def get_purchase_order(self):
        data = {
            "fk_vendor_id": self.vendor_id,
            "delivery_date": self.delivery_date_str,
            "items": {"item1": "Item 1", "item2": "Item 2"},
            "quantity": 10,
        }
        return PurchaseOrder.objects.create(**data)


class VendorsAPITestCase(BaseTest):
    def test_list_vendors(self):
        url = reverse("v1:vendors")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        url = reverse("v1:vendors")
        data = {
            "name": "Vendor B",
            "contact_details": "Contact",
            "address": "Address",
            "vendor_code": "B456",
        }
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deail_vendor(self):
        url = reverse("v1:vendors_detail", kwargs={"vendor_id": self.vendor_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse("v1:vendors_detail", kwargs={"vendor_id": self.vendor_id})
        data = {"name": "Vendor B"}
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        url = reverse("v1:vendors_detail", kwargs={"vendor_id": self.vendor_id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PurchaseOrdersAPITestCase(BaseTest):
    def test_create_purchase_order(self):
        url = reverse("v1:po")
        data = {
            "fk_vendor": self.vendor_id,
            "delivery_date": self.delivery_date_str,
            "items": {"item1": "Item 1", "item2": "Item 2"},
            "quantity": 10,
        }
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_purchase_order(self):
        url = reverse("v1:po")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_purchase_order(self):
        url = reverse("v1:po_detail", kwargs={"po_id": self.po_id.id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        url = reverse("v1:po_detail", kwargs={"po_id": self.po_id.id})
        data = {"delivery_date": "2024-05-12T14:39:03.206Z"}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_purchase_order(self):
        url = reverse("v1:po_detail", kwargs={"po_id": self.po_id.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PerformanceMetricsTaseCase(BaseTest):
    def test_ontime_delivery_rate(self):
        url = reverse("v1:po_status", kwargs={"po_id": self.po_id.id})
        data = {"status": PurchaseStatus.completed}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("v1:vendors_performance", kwargs={"vendor_id": self.vendor_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response_data = response.json()
        on_time_delivery_rate = response_data["data"]["on_time_delivery_rate"]
        expected_on_time_delivery_rate = 100.0
        self.assertEqual(on_time_delivery_rate, expected_on_time_delivery_rate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quality_rating_average(self):
        # update status PO to completed
        url = reverse("v1:po_status", kwargs={"po_id": self.po_id.id})
        data = {"status": PurchaseStatus.completed}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update quality_rating of PO
        url = reverse("v1:po_rating", kwargs={"po_id": self.po_id.id})
        data = {"quality_rating": 70}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the vendor performance
        url = reverse("v1:vendors_performance", kwargs={"vendor_id": self.vendor_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response_data = response.json()
        quality_rating_avg = response_data["data"]["quality_rating_avg"]
        expected_quality_rating_avg = 70.0
        self.assertEqual(quality_rating_avg, expected_quality_rating_avg)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_quality_rating_average(self):
        url = reverse("v1:po_rating", kwargs={"po_id": self.po_id.id})

        data = {"quality_rating": 70}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["message"], "Can't give rating for uncompleted order"
        )

    def test_average_response_time(self):
        # update issue_date of PO
        url = reverse("v1:po_detail", kwargs={"po_id": self.po_id.id})
        issue_date = datetime.now() + timedelta(days=2)
        issue_date_str = issue_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {"issue_date": issue_date_str}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # update acknowledgment_date of PO
        url = reverse("v1:po_acknowledge", kwargs={"po_id": self.po_id.id})
        acknowledgment_date = datetime.now() + timedelta(days=3)
        acknowledgment_date_str = acknowledgment_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {"acknowledgment_date": acknowledgment_date_str}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the vendor performance
        url = reverse("v1:vendors_performance", kwargs={"vendor_id": self.vendor_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response_data = response.json()
        average_response_time = response_data["data"]["average_response_time"]
        expected_average_response_time = 24
        rounded_actual = round(average_response_time, 2)
        rounded_expected = round(expected_average_response_time, 2)
        self.assertAlmostEqual(rounded_actual, rounded_expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_average_response_time(self):
        # update acknowledgment_date of PO
        url = reverse("v1:po_acknowledge", kwargs={"po_id": self.po_id.id})
        acknowledgment_date = datetime.now() + timedelta(days=3)
        acknowledgment_date_str = acknowledgment_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {"acknowledgment_date": acknowledgment_date_str}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["message"], "PO not issued to the vendor yet")

    def test_fullfilment_rate(self):
        # update status PO to completed
        url = reverse("v1:po_status", kwargs={"po_id": self.po_id.id})
        data = {"status": PurchaseStatus.completed}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the vendor performance
        url = reverse("v1:vendors_performance", kwargs={"vendor_id": self.vendor_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response_data = response.json()
        on_time_delivery_rate = response_data["data"]["on_time_delivery_rate"]
        fulfillment_rate = response_data["data"]["fulfillment_rate"]
        expected_fulfillment_rate = 100.0
        expected_on_time_delivery_rate = 100.0
        self.assertEqual(fulfillment_rate, expected_fulfillment_rate)
        self.assertEqual(on_time_delivery_rate, expected_on_time_delivery_rate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fullfilment_rate_with_issue_order(self):
        # update issue_order of PO
        url = reverse("v1:po_detail", kwargs={"po_id": self.po_id.id})
        data = {"issue_order": "some issue with the order"}
        response = self.client.put(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # update status PO to completed
        url = reverse("v1:po_status", kwargs={"po_id": self.po_id.id})
        data = {"status": PurchaseStatus.completed}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the vendor performance
        url = reverse("v1:vendors_performance", kwargs={"vendor_id": self.vendor_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response_data = response.json()
        on_time_delivery_rate = response_data["data"]["on_time_delivery_rate"]
        fulfillment_rate = response_data["data"]["fulfillment_rate"]
        expected_fulfillment_rate = 0
        expected_on_time_delivery_rate = 100.0
        self.assertEqual(fulfillment_rate, expected_fulfillment_rate)
        self.assertEqual(on_time_delivery_rate, expected_on_time_delivery_rate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
