from django.urls import path, re_path
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .gRPCclient import grpcFib, grpcLog


class fibonacci(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        return Response(
            data={
                "result": grpcFib(
                    {"ip": "0.0.0.0", "port": 8000, "order": int(request.data["order"])}
                )
            },
            status=200,
        )


class log(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(
            data={"history": grpcLog({"ip": "0.0.0.0", "port": 8081})}, status=200
        )


urlpatterns = [
    re_path(r"^fibonacci/?$", fibonacci.as_view()),
    re_path(r"^log/?$", log.as_view()),
]
