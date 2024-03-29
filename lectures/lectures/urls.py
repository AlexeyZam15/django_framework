"""
URL configuration for lectures project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from lecture_03.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prefix/', include('lecture_01.urls')),
    path('lec3/', include('lecture_03.urls')),
    path('', index),
    path('lec4/', include('lecture_04.urls')),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('lec6/', include('lecture_06.urls')),
]
