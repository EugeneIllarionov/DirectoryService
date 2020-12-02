from rest_framework.routers import DefaultRouter
from .views import DirectoryView

router = DefaultRouter()
router.register(r'dir', DirectoryView, basename='dir_url')
urlpatterns = router.urls
