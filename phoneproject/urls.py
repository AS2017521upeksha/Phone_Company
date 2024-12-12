app_name = 'payment_mgt'

from django.contrib import admin
from django.urls import path, include
from  . import settings
from django.conf.urls.static import static 
from store import views as storeviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', storeviews.storehome),
    path('store/', include('store.urls')),
    path('user_accounts/', include('user_accounts.urls')), 
    path('payment_mgt/', include(('payment_mgt.urls', 'payment_mgt'), namespace='payment_mgt')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
