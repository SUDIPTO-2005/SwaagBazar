from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Product, Contact, Orders, orderupdate
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json
from math import ceil
from django.http import JsonResponse

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def index(request):
    products = Product.objects.all()
    allProd = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProd.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProd}
    return render(request, 'shop/index1.html', params)

def searchMatch(query, item):
    if query in item.prod_name.lower or query in item.category.lower:
        return True
    else:
        return False
    
def search(request):
    query=request.GET.get('search','')
    products = Product.objects.filter(prod_name__icontains=query)
    allProd = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = products.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!=0:
            allProd.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProd,'msg':''}
    if len(allProd)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)
def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(ord_id=orderId, email=email)
            if len(order)>0:
                updates = orderupdate.objects.filter(order_id=orderId)
                update_list = []
                for item in updates:
                    update_list.append({
                        'text': item.update_desc,
                        'time': item.timestamp.strftime("%Y-%m-%d")
                    })
                response = json.dumps({"status":"success", "updates": update_list, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')

def prodview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product': product[0]})
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(
            items_json=items_json,
            amount=amount,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )
        order.save()

        razorpay_order = client.order.create({
            "amount": int(float(amount) * 100),
            "currency": "INR"
        })

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        print("RAZORPAY ORDER CREATED:", razorpay_order["id"])

        context = {
            "order": order,
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "amount": int(float(amount) * 100),
            "currency": "INR"
        }

        return render(request, "shop/razorpay.html", context)
        

    return render(request, "shop/checkout.html")


# def handlerequest(request):
#     if request.method == "POST":
#         print("PAYMENTHANDLER CALLED")
#         print("POST DATA:", request.POST)

#         razorpay_payment_id = request.POST.get("razorpay_payment_id")
#         razorpay_order_id = request.POST.get("razorpay_order_id")
#         razorpay_signature = request.POST.get("razorpay_signature")

#         if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
#             return HttpResponse("Missing payment data")

#         params_dict = {
#             "razorpay_order_id": razorpay_order_id,
#             "razorpay_payment_id": razorpay_payment_id,
#             "razorpay_signature": razorpay_signature
#         }

#         try:
#             client.utility.verify_payment_signature(params_dict)

#             order = Orders.objects.get(razorpay_order_id=razorpay_order_id)
#             order.razorpay_payment_id = razorpay_payment_id
#             order.razorpay_signature = razorpay_signature
#             order.paid = True
#             order.save()

#             update = orderupdate(order_id=order.ord_id, update_desc="Payment successful")
#             update.save()

#             send_mail(
#                 subject='Order Placed',
#                 message=f"""Your order has been successfully placed and payment received.

# Order ID: {order.ord_id}
# Amount: ₹{order.amount}

# Thank you for shopping with us!""",
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[order.email],
#                 fail_silently=False,
#             )

#             return render(request, "shop/paymentstatus.html", {"order": order})

#         except Orders.DoesNotExist:
#             return HttpResponse("Order not found")

#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponse("Signature verification failed")

#         except Exception as e:
#             print("ERROR:", str(e))
#             return HttpResponse("Error: " + str(e))

#     return HttpResponse("Invalid request method")

@csrf_exempt
def handlerequest(request):
    print("HANDLEREQUEST CALLED")
    print("METHOD:", request.method)
    print("POST DATA:", request.POST)

    if request.method != "POST":
        return redirect("/shop/payment-failed/")

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    print("payment_id:", razorpay_payment_id)
    print("order_id:", razorpay_order_id)
    print("signature:", razorpay_signature)

    if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
        print("Missing payment data")
        return redirect("/shop/payment-failed/")

    params_dict = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        print("SIGNATURE VERIFIED")

        order = Orders.objects.get(razorpay_order_id=razorpay_order_id)
        print("ORDER FOUND:", order.ord_id)

        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.paid = True
        order.save()

        orderupdate.objects.create(
            order_id=order.ord_id,
            update_desc="Payment successful"
        )

        try:
            send_mail(
                subject="Order Placed Successfully",
                message=f"""Your payment was successful.

Order ID: {order.ord_id}
Amount: ₹{order.amount}

Thank you for shopping with us!""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=True,
            )
        except Exception as mail_error:
            print("EMAIL ERROR:", str(mail_error))

        return redirect(f"/shop/payment-success/?order_id={order.ord_id}")

    except Orders.DoesNotExist:
        print("ORDER NOT FOUND")
        return redirect("/shop/payment-failed/")

    except razorpay.errors.SignatureVerificationError as e:
        print("SIGNATURE ERROR:", str(e))
        return redirect("/shop/payment-failed/")

    except Exception as e:
        print("GENERAL ERROR:", str(e))
        return redirect("/shop/payment-failed/")


def payment_success(request):
    order_id = request.GET.get("order_id")
    order = None

    if order_id:
        try:
            order = Orders.objects.get(ord_id=order_id)
        except Orders.DoesNotExist:
            order = None

    return render(request, "shop/payment_success.html", {"order": order})


def payment_failed(request):
    return render(request, "shop/payment_failed.html")