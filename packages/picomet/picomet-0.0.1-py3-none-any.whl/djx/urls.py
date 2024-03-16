from django.conf import settings
from django.conf.urls.static import static

urlpatterns = []
urlpatterns += static("/assets/", document_root=settings.BASE_DIR / ".djx/assets")
