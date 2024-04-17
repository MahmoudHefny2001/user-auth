from django.shortcuts import render

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import views, status, viewsets, response
from rest_framework.permissions import AllowAny

from .serializers import ConactFormSerializer


class SendForm(views.APIView):
    permission_classes = [AllowAny,]
    serializer_class = ConactFormSerializer

    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            data={
                "message": "Your message has been sent successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )