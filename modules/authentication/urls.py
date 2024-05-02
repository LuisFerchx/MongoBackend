from django.urls import re_path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    re_path(r"", include(router.urls)),
]
