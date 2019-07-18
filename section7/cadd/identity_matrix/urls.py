from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('identity', views.identity, name='identity'),
    path('matrix', views.matrix, name='matrix')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
