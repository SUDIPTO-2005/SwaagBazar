from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('',views.index,name='ShopHome'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='Contact'),
    path('tracker/',views.tracker,name='TrackingStatus'),
    path('search/',views.search,name='Search'),
    path('products/<int:myid>',views.prodview,name='Productview'),
    path('checkout/',views.checkout,name='Checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest'),
    path("payment-success/", views.payment_success, name="payment_success"),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)