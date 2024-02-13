"""
URL configuration for seminars project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('seminar_01/', include('seminar_01.urls')),
                  path('homework_01/', include('homework_01.urls')),
                  path('seminar_03/', include('seminar_03.urls')),
                  path('homework_03/', include('homework_03.urls')),
                  path('seminar_04/', include('seminar_04.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
