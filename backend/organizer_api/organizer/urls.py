from django.urls import path

from organizer_api.settings import MEDIA_ROOT, MEDIA_URL
from . import views
from django.conf.urls import url

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.apiOverview, name="api_overview"),
    # path('scrap-list', views.scrapList, name="scrap-list"),
    # path('scrap-detail/<str:pk>/', views.scrapDetail, name="scrap-detail"),
    # path('scrap-create/', views.scrapCreate, name="scrap-create"),
    # path('scrap-delete/<str:pk>/', views.scrapDelete, name="scrap-delete"),
    url(r'^scrap$', views.Api),
    url(r'^scrap$/([0-9]+)$', views.Api),
    url(r'^scrap/save', views.SaveFile)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
