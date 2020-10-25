
from django.contrib import admin
from django.urls import path,include
from user.views import indexView,contactView,storeView,cartView,checkoutView, productDetailView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',indexView,name='home'),
    path('contact/',contactView,name='contact'),
    path('products/',storeView,name='products'),
    path('products/<int:pk>',productDetailView,name='product_detail'),
    path('cart/',cartView,name='cart'),
    path('checkout/',checkoutView,name='checkout'),
    path('user/',include('user.urls')),
] 

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




