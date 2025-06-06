from django.shortcuts import render,redirect
from .models import Products, ProductImage, Category, Wishlist, Carts


# Create your views here.
def index(req):
    allproducts = Products.objects.all()
    allproductimages = ProductImage.objects.all().first()
    allcategory = Category.objects.all()
    print(allproducts)
    print(allproductimages,)
    context = {"allproducts":allproducts,"allproductimages":allproductimages,"allcategory":allcategory}
    return render(req, "index.html",context)

from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser


def signup(req):
    print(req.method)
    if req.method == "POST":
        print(req.method)
        uname = req.POST.get("uname")
        uemail = req.POST.get("uemail")
        upass = req.POST.get("upass")
        ucpass = req.POST.get("ucpass")
        print(uname, uemail, upass, ucpass)
        user = CustomUser.objects.values_list("username", flat=True)
        print(user)
        chkemail = CustomUser.objects.values_list("email", flat=True)
        print(chkemail)

        if upass != ucpass:
            # errmsg="Password and Confirm Password doesn't match. Try again"
            # context={'errmsg':errmsg}
            # return render(req,'signup.html',context)

            messages.error(
                req, "Password and Confirm Password doesn't match.TRY again "
            )
            return render(req, "signup.html")
        elif uname == upass:
            messages.error(req, " Username and Password be different")
            return render(req, "signup.html")
        elif uname in user:
            messages.error(req, " Username already exists. Try again")
            return render(req, "signup.html")
        elif uemail in chkemail:
            messages.error(req, " Email already exists")
            return render(req, "signup.html")

        newuser = CustomUser.objects.create(username=uname, email=uemail, password=upass, is_customer=True)
        newuser.set_password(upass)
        newuser.save()
        print(CustomUser.objects.all())

        messages.success(req, "Registration done Successfully!! ")
        return redirect("signin")

    else:
        print(req.method)
        return render(req, "signup.html")


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

def signin(req):
    if req.method=="POST":
        user_type=req.POST.get("user_type")
        uemail = req.POST.get("uemail")
        upass = req.POST.get("upass")
        print(user_type,uemail,upass)

        try:
            chkemail = CustomUser.objects.get(email=uemail)
            print(chkemail)
            if chkemail.check_password(upass):
                login(req, chkemail)
                if user_type=="admin":
                    if chkemail.is_staff:
                        return redirect("/admin")
                    else:
                        messages.error(req, "Invalid email or password")
                        return render(req, "signin.html")
                else:
                    return redirect('/')
            else:
                messages.error(req, "Invalid email or password")
                return render(req, "signin.html")
        except CustomUser.DoesNotExist:
            messages.error(req, "User Not exists")
            return render(req, "signin.html")
    else:
        return render(req,"signin.html")
    

def userlogout(req):
    logout(req)
    return redirect("/")

def seller(req):
    user = req.user
    chkuser = CustomUser.objects.get(username = user)
    print(chkuser)
    if chkuser.is_seller:
        return render(req, "seller.html")
    else:
        return render(req, "seller_payment.html")

def seller_payment(req):
    if req.method == "POST":
        chkuser = CustomUser.objects.get(username = req.user)
        chkuser.is_seller = True
        chkuser.save()
        return redirect("seller")
    else:
        client = razorpay.Client(
            auth=(settings.RZPAY_KEY_ID, settings.RZPAY_KEY_SECRET)
        )
        amount_paise = 1000 * 100
        razorpay_order = client.order.create(
            {"amount": amount_paise, "currency": "INR"}
        )
        context = {"amount":amount_paise, "orderid":razorpay_order["id"]}
        return render(req, "seller_payment.html",context)

from django.db.models import Q

def searchproducts(req):
    query=req.GET["q"]
    if query:
        allproducts = Products.objects.filter(
            Q(productname__icontains=query) | Q(description__icontains=query )
        )
        print(allproducts)

        if len(allproducts) == 0:
            messages.error(req, "No results found!")
    else:
        allproducts = Products.objects.all()
    allcategory = Category.objects.all()
    print(allcategory)

    context = {"allproducts":allproducts,"allcategory":allcategory}
    return render(req, "index.html", context)

def electronic_search(req):
    ele_category = Category.objects.filter(name="Electronics").first()
    allproducts = Products.objects.filter(category=ele_category)
    allcategory = Category.objects.all()
    print(allproducts)

    if len(allproducts) == 0:
        messages.error(req, "No results found!")

    context = {"allproducts":allproducts,"allcategory":allcategory}
    return render(req, "index.html", context)

def clothes_list(req):
    allproducts=Products.productmanager.clothes_search()
    print(allproducts)
    allcategory = Category.objects.all()

    if len(allproducts) == 0:
        messages.error(req, "No results found!")

    context = {"allproducts":allproducts,"allcategory":allcategory}
    return render(req, "index.html", context)

def shoes_list(req):
    allproducts=Products.productmanager.shoes_search()
    print(allproducts)
    allcategory = Category.objects.all()

    if len(allproducts) == 0:
        messages.error(req, "No results found!")

    context = {"allproducts":allproducts,"allcategory":allcategory}
    return render(req, "index.html", context)

def babyproducts_list(req):
    allproducts=Products.productmanager.baby_products_search()
    print(allproducts)
    allcategory = Category.objects.all()

    if len(allproducts) == 0:
        messages.error(req, "No results found!")

    context = {"allproducts":allproducts,"allcategory":allcategory}
    return render(req, "index.html", context)

def searchbyprice_range(req):
    if req.method=="GET":
        return render(req, 'index.html')
    else:
        r1=req.POST.get("min")
        r2=req.POST.get("max")
        print(r1,r2)
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts=Products.productmanager.price_range(r1,r2)
            print(allproducts)
            if len(allproducts)==0:
                messages.error(req, 'No results found')
        else:
            allproducts=Products.objects.all()
        
        allcategory = Category.objects.all()
        context = {"allproducts":allproducts, "allcategory":allcategory}
        return render(req, "index.html", context)
    
def sortingbyprice(req):
    sortoption = req.GET["sort"]
    if sortoption == "low_to_high":
        allproducts=Products.objects.order_by("price")
    elif sortoption == "high_to_low":
        allproducts=Products.objects.order_by("-price")
    else:
        allproducts=Products.objects.all()
    
    allcategory=Category.objects.all()
    context = {"allproducts":allproducts,"allcategory":allcategory}
    return render(req, 'index.html', context)

def productdetails(req, productid):
    product = Products.objects.get(productid=productid)
    productimage = ProductImage.objects.filter(productid=productid)
    context = {'product':product, 'productimage':productimage}
    return render(req, "productdetails.html", context)

def show_wishlist(req):
    if req.user.is_authenticated:
        user = req.user
        wishlist_item = Wishlist.objects.filter(user=user)
        context={'wishlist_item':wishlist_item}
        if len(wishlist_item) == 0:
            messages.error(req, "No Items Selected")
        return render(req, "wishlist_item.html",context)
    else:
        return redirect("signin")
    
from django.shortcuts import get_object_or_404
def addtowishlist(req, productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid=productid)
        if not Wishlist.objects.filter(user=req.user, productid=productid).exists():
            Wishlist.objects.create(user=user, productid=product)
            messages.success(req,"Product added to wishlist")
        else:
            messages.info(req,"Product is already in wishlist")
        return redirect("show_wishlist")
    else:
        return redirect("signin")
    
def removewishlist(req, productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid=productid)
        wishlist_item = Wishlist.objects.filter(user=user,productid=product)
        wishlist_item.delete()
        messages.success(req, "Product Removed from wishlist")
        return redirect("show_wishlist")
    else:
        return redirect("signin")
    
from datetime import datetime,timedelta
from .models import UserProfile, Address
def showcarts(req):
    if req.user.is_authenticated:
        user = req.user
        cart_item = Carts.objects.filter(user=user)
        currdate = datetime.now().date()
        futuredate = currdate+timedelta(days=4)
        print(currdate)

        totalitems = cart_item.count()
        totalamount = sum(x.productid.price*x.qty for x in cart_item)
        has_profile = UserProfile.objects.filter(user=user).exists()
        has_address = Address.objects.filter(user=user).exists()

        context = {
            "cart_item":cart_item,
            "futuredate":futuredate, 
            "totalitems":totalitems, 
            "totalamount":totalamount, 
            "has_profile":has_profile, 
            "has_address":has_address
        }
        return render(req,"showcarts.html",context)
    else:
        return redirect("signin")
    
def updateqty(req, qv, productid):
    product = get_object_or_404(Products,productid=productid)
    allcarts = Carts.objects.filter(productid=productid, user=req.user)
    cart_item = allcarts.first()
    if qv == 1:
        if cart_item.qty<product.qty_available:
            cart_item.qty+=1
            cart_item.save()
        else:
            messages.error(req, "Only Limited Stock Available")
    else:
        if cart_item.qty>1:
            cart_item.qty-=1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect("showcarts")

def addtocart(req, productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid=productid)
        cartitem, created = Carts.objects.get_or_create(user=user, productid=product)
        new_qty = cartitem.qty + 1 if not created else 1
        if new_qty>product.qty_available:
            messages.error(req, 'Cannot add more item (Limited stock available)')
            return redirect('showcarts')
        cartitem.qty=new_qty
        cartitem.save()
        return redirect('showcarts')
    else:
        return redirect('signin')

def removetocart(req, productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid=productid)
        cartitem = Carts.objects.filter(user=user, productid=product)
        cartitem.delete()
        messages.success(req,"Product removed from cart.")
        return redirect("showcarts")
    else:
        return redirect('signin')
    
def myprofile(req):
    user = req.user
    userprofile = UserProfile.objects.filter(user=user).first()
    addresses= Address.objects.filter(user=user)
    context = {'user':user, 'userprofile':userprofile, "addresses":addresses}
    return render(req, 'myprofile.html', context)

from datetime import datetime
from django.utils import timezone
def addprofile(req):
    user = req.user
    if req.method == "POST":
        mobile = req.POST.get("mobile")
        gender = req.POST.get("gender")
        dob = req.POST.get("dob")
        photo = req.FILES["photo"]
        if dob:
            dob_date=datetime.strptime(dob, '%Y-%m-%d').date()
            today = timezone.now().date()
            if dob_date>today:
                messages.error(req, 'Date of Birth can not be todays or futrure date.')
            age = today.year-dob_date.year-((today.month, today.day)<(dob_date.month,dob_date.day))
            print(age)
            if age<18:
                messages.error(req,'You must be at least 18 years old to create proofile.')
                return render(req, 'addprofile.html')


        UserProfile.objects.create(user=user, mobile= mobile, gender=gender, dob=dob, photo=photo)
        return redirect("myprofile")
    else:
        return render(req, "addprofile.html")        
    
def editprofile(req,profileid):
    profile=get_object_or_404(UserProfile, id = profileid)
    if req.method=="POST":
        profile.mobile=req.POST["mobile"]
        profile.gender=req.POST["gender"]
        profile.dob=req.POST["dob"]
        if "photo" in req.FILES:
            profile.photo = req.FILES["photo"]
        profile.save()
        return redirect('myprofile')
    return render(req, "editprofile.html", {"userprofile":profile})

from .models import City,Country

def addaddress(req):
    user=req.user
    if req.method=="POST":
        address=req.POST["address"]
        city=req.POST["city"]
        country=req.POST["country"]
        pincode= req.POST["pincode"]
        Address.objects.create(user=user,address=address,city_id=city,country_id=country,pincode=pincode)
        return redirect('myprofile')
    cities = City.objects.all
    countries = Country.objects.all
    context= {'cities':cities, 'countries':countries}
    return render(req, "addaddress.html",context)

def deleteaddress(req, addressid):
    address = get_object_or_404(Address, id=addressid)
    address.delete()
    return redirect("myprofile")


def editaddress(req, addressid):
    address = get_object_or_404(Address, id=addressid)
    if req.method == "POST":
        address.address = req.POST["address"]
        city_id = req.POST["city"]
        country_id = req.POST["country"]
        address.pincode = req.POST["pincode"]

        if city_id:
            address.city_id = city_id

        if country_id:
            address.country_id = country_id

        address.save()
        return redirect("myprofile")

    citites = City.objects.all()
    countries = Country.objects.all()
    context = {"address": address, "cities": citites, "countries": countries}
    return render(req, "editaddress.html", context)

def checkout(req):
    cart_item=Carts.objects.filter(user=req.user)
    if not cart_item.exists():
        messages.error(req,'Please add items into cart, then proceed to checkout.')
        return redirect("showcarts")
    
    cartdata=[]
    total = 0
    for item in cart_item:
        subtotal=item.qty*item.productid.price
        cartdata.append(
            {
                'productname':item.productid.productname,
                'qty':item.qty,
                'price': item.productid.price,
                'subtotal':subtotal,
            }
        )
        total+=subtotal
    profile= UserProfile.objects.filter(user=req.user).first()
    return render(req, 'checkout.html',{
        'cartdata':cartdata,
        'profile':profile,
        'address':Address.objects.filter(user=req.user),
        'total':total,
        'mobile':profile.mobile,
        'user':req.user,
        'email':req.user.email
    })

def checkoutsingle(req, productid):
    user = req.user
    address = Address.objects.filter(user=user)
    cartitem = Carts.objects.get(user=user, productid__productid=productid)
    cartdata = [
    {
        "productid": cartitem.productid.productid,  # <-- Add this
        "productname": cartitem.productid.productname,
        "qty": cartitem.qty,
        "price": cartitem.productid.price,
        "subtotal": cartitem.qty * cartitem.productid.price,
    }
    ]
    total = cartdata[0]["subtotal"]
    profile = UserProfile.objects.filter(user=user).first()
    return render(
        req,
        "checkout.html",
        {
            "cartdata": cartdata,
            "profile": profile,
            "address": address,
            "total": total,
            "mobile": profile.mobile,
            "user": req.user,
            "email": req.user.email,
        },
    )

import razorpay
from django.conf import settings

def placeorder(req):
    if req.method=="POST":
        user=req.user
        address_id=req.POST.get("address_id")
        total=0
        print(address_id)
        address=get_object_or_404(Address,id=address_id,user=user)
        profile=UserProfile.objects.filter(user=user).first()
        product_id= req.POST.get('product_id')
        cartdata=[]
        if product_id:
            cartitem=get_object_or_404(Carts,user=user,productid__productid=product_id)
            subtotal=cartitem.qty*cartitem.productid.price
            total+=subtotal
            req.session["product_id"] = product_id
            req.session['singleorderamount']=total*100
            cartdata.append({
                'productname':cartitem.productid.productname,
                'qty':cartitem.qty,
                'price':cartitem.productid.price,
                'subtotal':subtotal
            })
        else:
            cart_items=Carts.objects.filter(user=user)
            for item in cart_items:
                subtotal=item.qty*item.productid.price
                total+=subtotal
                cartdata.append({
                    "productname":item.productid.productname,
                    'qty':item.qty,
                    'price':item.productid.price,
                    'subtotal':subtotal
                })
            req.session['allorderamount']=total*100
        
        amount_paise=total*100
        client = razorpay.Client(auth=(settings.RZPAY_KEY_ID, settings.RZPAY_KEY_SECRET))

        # data = { "amount": amount_paise, "currency": "INR", "receipt": "order_rcptid_11" }
        # payment = client.order.create(data=data) #Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
        razorpay_order = client.order.create({
            'amount':amount_paise,
            'currency':'INR'
        })
        return render(req,'payment.html',{
            "profile": profile,
            "address": address,
            "cartdata": cartdata,
            "total": total,
            "user": user,
            "amount":amount_paise,
            "orderid":razorpay_order["id"],
        })
    else:
        return redirect('checkout')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import date
from .models import Order
from razorpay.errors import SignatureVerificationError

@csrf_exempt
def payment(req):
    if req.method == "POST":
        try:
            data = json.loads(req.body)
            print("Parsed data:", data)

            payment_id = data.get("razorpay_payment_id")
            order_id = data.get("razorpay_order_id")
            razorpay_signature = data.get("razorpay_signature")

            if not all([payment_id, order_id, razorpay_signature]):
                return JsonResponse({"status": "missing_data"}, status=400)

            client = razorpay.Client(
                auth=(settings.RZPAY_KEY_ID, settings.RZPAY_KEY_SECRET)
            )
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": razorpay_signature,
            }

            try:
                client.utility.verify_payment_signature(params_dict)
                user = req.user
                profie = UserProfile.objects.get(user=user)
                address = Address.objects.filter(user=user).first()
                cart_items = Carts.objects.filter(user=user)

                if req.session.get("product_id"):
                    product_id = req.session.get("product_id")
                    cart = Carts.objects.filter(productid=product_id).first()
                    orderamount = req.session.get("singleorderamount")
                    Order.objects.create(
                        user=user,
                        productid=cart.productid,
                        qty=cart.qty,
                        orderdate=datetime.now(),
                        address=address,
                        paymentstatus="Paid",   
                        orderstatus="Delivered",
                        orderamount=orderamount/100,
                    )
                    cart.delete()
                    del req.session["product_id"]
                else:
                    for item in cart_items:
                        Order.objects.create(
                            user=user,
                            productid=item.productid,
                            qty=item.qty,
                            orderdate=datetime.now(),
                            address=address,
                            paymentstatus="Paid",
                            orderstatus="Delivered",
                            orderamount=item.productid.price,
                        )
                    cart_items.delete()
                req.session['order_id']=order_id
                req.session['payment_id']=payment_id
                req.session['amount']=client.order.fetch(order_id)['amount']
                return JsonResponse(
                    {"status": "success", "redirect_url": "/payment_success/"}
                )

            except SignatureVerificationError:
                return JsonResponse({"status": "invalid_json"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "invalid_json"}, status=400)

    return redirect("showcarts")



from django.core.mail import send_mail
def payment_success(req):
    order_id = req.session.get('order_id')
    payment_id = req.session.get('payment_id')
    amount = req.session.get('amount')
    user=req.user

    subject = "Order Confirmation - Thank You for Your Purchase!"
    msg = f'Hi {user},\n\nYour order #{order_id} has been successfully placed.\n\nTotal amount:{float(amount)/100}\n\nThank you for shopping with us!\n\n- Team Amazon'
    emailfrom = settings.EMAIL_HOST_USER
    receiver = [user.email]

    send_mail(subject, msg, emailfrom, receiver)
    context = {'order_id':order_id, 'payment_id':payment_id,'amount':(float(amount)/100),'user':user,}
    return render(req, 'payment_success.html',context)


def showorders(req):
    user = req.user
    orders = Order.objects.filter(user=user).select_related('productid','address').order_by('-orderdate')
    for order in orders:
        order.orderamount = order.qty*order.productid.price
        if not order:
            order.orderstatus="Pending"
            order.paymentstatus="Unpaid"
        else:
            order.orderstatus="Delivered"
            order.paymentstatus="Paid"
    return render(req, "showorders.html", {"orders":orders})
