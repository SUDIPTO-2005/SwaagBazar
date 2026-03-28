from django.contrib import admin

from .models import Product
admin.site.register(Product)

from .models import Contact
admin.site.register(Contact)

from .models import Orders
admin.site.register(Orders)

from .models import orderupdate
admin.site.register(orderupdate)
