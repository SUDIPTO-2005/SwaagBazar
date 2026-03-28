from django.db import models

class Product(models.Model):
    prod_id=models.AutoField
    prod_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=320)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="shop/images",default="")
    def __str__(self):
         return self.prod_name

class Contact(models.Model):
     msg_id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=30,default="")
     email=models.CharField(max_length=50,default="")
     phone=models.CharField(max_length=20)
     desc=models.CharField(max_length=200,default="")

     def __str__(self):
          return self.name
class Orders(models.Model):
    ord_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, default="")
    
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
          return str(self.ord_id)
class orderupdate(models.Model):
     update_id=models.AutoField(primary_key=True)
     order_id=models.IntegerField(default='')
     update_desc=models.CharField( max_length=5000)
     timestamp=models.DateField(auto_now_add=True)

     def __str__(self):
          return self.update_desc[0:8]+"..."
     