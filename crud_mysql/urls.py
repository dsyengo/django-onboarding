from django.urls import include, path
from .views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)


urlpatterns = [
   path('', include(router.urls))
]