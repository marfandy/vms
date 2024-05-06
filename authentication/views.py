from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from authentication.models import Account
from authentication.serializers import SignInResponseSerializer, SignInSerializer


class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    @swagger_auto_schema(tags=["User"])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signin_response_serializer = SignInResponseSerializer
        username = serializer.data.get("username").lower()
        user = Account.objects.get(username=username)
        return Response(signin_response_serializer(user).data)
