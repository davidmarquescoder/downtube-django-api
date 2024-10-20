from django.contrib import admin
from django.urls import path
from downtube.api.controller import DowntubeController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('download/', DowntubeController.as_view(), name='download_video'),
]
