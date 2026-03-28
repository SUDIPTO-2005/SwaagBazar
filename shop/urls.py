from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('',views.index,name='ShopHome'),
    path("load-data/", views.load_shop_data, name="load_data"),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='Contact'),
    path('tracker/',views.tracker,name='TrackingStatus'),
    path('search/',views.search,name='Search'),
    path('products/<int:myid>',views.prodview,name='Productview'),
    path('checkout/',views.checkout,name='Checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)