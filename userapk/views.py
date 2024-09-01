from django.shortcuts import render,redirect,get_object_or_404
from adminapk.models import Category,Product 
from .models import Customer,Cart,Address,Order
from django.contrib import messages
import random
from django.core.mail import send_mail
from .models import customer_otp
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponseBadRequest


def home_view(request):
    customer_id = request.session.get('customer_id')
    products = Product.objects.all()
    cart_item_count = 0
    cart_items = []

    if customer_id:
        customer = Customer.objects.get(id=customer_id)
        cart_items = Cart.objects.filter(customer=customer).values_list('product_id', flat=True)
        cart_item_count = cart_items.count()
    
    return render(request, 'index_page.html', {
        'products': products,
        'cart_items': cart_items,
        'cart_item_count': cart_item_count,
        'cats': Category.objects.all(),
    })

def user_signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        father = request.POST.get('father')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        phone = request.POST.get('Phone')
        image = request.FILES.get('image')

       
        customer = Customer(fname=fname,lname=lname,father=father,email=email,pass1=pass1,Phone=phone,image=image)
        customer.save()

        return redirect('/user_login') 

    return render(request,"user_signup.html")


def user_login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
 
        try:
            customer=Customer.objects.get(email=email)
            if customer.pass1 == password:
                request.session['customer_id']=customer.id
                request.session['customer_image']=customer.image.url
                return redirect('/') 
            else:
                messages.error(request, 'Invalid password')
        except Exception as e:
            messages.error(request, 'Invalid email')
    
    return render(request, "user_login.html")


def user_logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
        del request.session['customer_image']
    return redirect('/')


def add_to_cart(request, product_id):
    customer = Customer.objects.get(id=request.session['customer_id'])
    product = Product.objects.get(id=product_id)
    
    cart, created = Cart.objects.get_or_create(customer=customer, product=product)
    if not created:
        cart.quantity += 1
        cart.save()
    
    return redirect('/')

def remove_from_cart(request, product_id):
    customer = Customer.objects.get(id=request.session['customer_id'])
    product = Product.objects.get(id=product_id)
    
    Cart.objects.filter(customer=customer, product=product).delete()
    
    return redirect('/')  




def view_cart(request):
    print(request.user)
    if not request.session.get('customer_id'):
        messages.error(request, 'You need to log in first.')
        return redirect('/user_login')
       
    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    cart_items = Cart.objects.filter(customer=customer)
    return render(request, 'cart.html', {'cart_items': cart_items})

def profile(request):
    if not request.session.get('customer_id'):
        messages.error(request, "Please log in first")
        return redirect('user_login')

    cid = request.session['customer_id']
    customer = Customer.objects.get(id=cid)
    
    return render(request, "profile_page.html", {'customer': customer})

    
def update_product(request, pid):
    if request.method == "POST":
        val = request.POST.get('action')
        try:
            item = Cart.objects.get(product=pid)
        except Cart.DoesNotExist:
            print("Item not found in cart")
            return redirect('/view_cart')
        except Exception as e:
            return HttpResponse(e)

        if val == "increase":
            item.quantity += 1
            item.save()
            print("Quantity increased")
        elif val == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                print("Quantity decreased")
            else:     
                item.delete()
                print("Item deleted due to quantity 0")
                return redirect('/view_cart')
        if val == "delete":
            item.delete()
            print("Item deleted")
        
        cid=request.session['customer_id']
        customer=Customer.objects.get(id=cid)
        request.session['item_quantity']=Cart.objects.filter(customer=customer).count() 
        
        
        # item.save()
        return redirect('/view_cart')

    return redirect('/view_cart')




def error_view(request,exception):
    print("started")
    return render(request, 'error404.html', {}, status=404)

def forgot_cutomer_password(request):
    if request.method=="POST":
        email=request.POST.get('email')

        try:
            customer=Customer.objects.get(email=email)
        except:
            messages.error(request,"this email doesn't exist")
            return render(request,"forgot_password.html")
        
        otp=random.randint(100000,999999)
        customer_otp.objects.create(customer=customer,otp=otp)

        send_mail(
            'Your OTP for Password Reset',
            f'Your OTP is {otp}',
            'Sumitshukla7318@gmail.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, 'OTP has been sent to your email.')
        return redirect('/reset_password')

    return render(request,"forgot_password.html")

def reset_customer_password(request):
    if request.method=="POST":
        otp=request.POST.get('otp')
        new_password=request.POST.get('new_password')

        try:
            customer=customer_otp.objects.get(otp=otp)
        except:
            messages.error(request,"Invalid Otp")
            return render(request,"reset_admin_pass.html")
        
        customer.customer.pass1=new_password
        customer.customer.save()
        messages.success(request, 'Password has been reset successfully.')
        return redirect('/user_login')

    return render(request,"reset_admin_pass.html")

def filter_products(request):
    category_id = request.POST.get('category')
    price_range = request.POST.get('price')

    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if price_range:
        min_price, max_price = price_range.split('-')
        max_price = float(max_price) if max_price != '+' else float('inf')
        products = products.filter(price__gte=float(min_price), price__lte=max_price)

    categories = Category.objects.all()

    return render(request, 'index_page.html', {'products': products, 'cats': categories})

def update_profile(request):
    print("fuction executed sucessfully")
    if request.method=="POST":
        fn=request.POST.get('full_name')
        e=request.POST.get('email')
        p=request.POST.get('phone')
        pwd=request.POST.get('password')
        cpwd=request.POST.get('confirm_password')

        obj=Customer.objects(fname=fn,email=e,pass1=p)


def order_history(request):
    if not request.session.get('customer_id'):
        messages.error(request, 'You need to log in first.')
        return redirect('/user_login')
       
    customer_id = request.session['customer_id']
    customer=Customer.objects.get(id=customer_id)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'order_history.html', {'orders': orders})

def address_management(request):
    if not request.session.get('customer_id'):
        messages.error(request, "You need to login first")
        return redirect('user_login')
    
    cid = request.session['customer_id']
    customer = Customer.objects.get(id=cid)
    addresses = Address.objects.filter(customer=customer)

    return render(request, 'address_management.html', {'addresses': addresses})

def add_address(request):
    if request.method == "POST":
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'

        cid = request.session['customer_id']
        customer = Customer.objects.get(id=cid)
        Address.objects.create(
            customer=customer,
            street_address=street_address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=is_default
        )
        return redirect('address_management')
    
    return render(request, "add_address.html")


def edit_address(request,address_id):
    
    address = Address.objects.get(id=address_id)
       

    if request.method == 'POST':
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'

        address.street_address = street_address
        address.city = city
        address.state = state
        address.postal_code = postal_code
        address.country = country
        address.is_default = is_default
        address.save()

        return redirect('address_management')

    return render(request, 'edit_address.html', {'address': address})



def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id)
        address.delete()
        return redirect('address_management')

    return redirect('address_management')


def order_summary_view(request):
     customer = request.session.get('customer_id')  
     cart_items = Cart.objects.filter(customer_id=customer)
    
     if not cart_items:
        return redirect('/view_cart') 

     return render(request, 'order_summary.html', {'cart_items': cart_items})

def select_address_view(request):
    customer = request.session.get('customer_id')
    addresses = Address.objects.filter(customer_id=customer)
    c=Customer.objects.get(id=customer)
    return render(request, 'select_address.html', {'addresses': addresses,'customer':c})

def payment_view(request):
    if request.method == "POST":
        address_id = request.POST.get('address')
        request.session['address_id'] = address_id

        return render(request, 'payment.html')
    else:
        return redirect('select_address')
    


def place_order_view(request):
   
    customer_id = request.session.get('customer_id')
    address_id = request.session.get('address_id')
    
    if not customer_id or not address_id:
        messages.error(request, "Please select an address and make sure you're logged in.")
        return redirect('/view_cart') 

    customer = Customer.objects.get(id=customer_id)
    address = Address.objects.get(id=address_id)
    
    # Get the cart items for the customer
    cart_items = Cart.objects.filter(customer=customer)
    
    if not cart_items:
        messages.error(request, "Your cart is empty. Cannot place an order.")
        return redirect('view_cart')  # Redirect to cart page if cart is empty
    

    total_price = cart_items.aggregate(total_price=Sum('product__price'))['total_price']
    

    for item in cart_items:
        Order.objects.create(
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity,
            status='Pending'
        )
    
    
    

    order_details = [
        {
            'product': item.product,
            'quantity': item.quantity,
            'price': item.product.price,
            'total': item.product.price * item.quantity
        }
        for item in Cart.objects.filter(customer=customer)
    ]
    print(order_details)


    cart_items.delete()
    

    return render(request, 'order_confirmation.html', {
        'customer': customer,
        'address': address,
        'order_details': order_details,
        'total_price': total_price
    })

    
def confirm_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == order.otp:
            order.status = 'Placed'
            order.confirmed_at = timezone.now()
            order.save()
            messages.success(request, 'Order confirmed successfully!')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
        return redirect('order_history')
    else:
        otp = str(random.randint(100000, 999999))
        order.otp = otp
        order.save()
        send_mail(
            'Your Order OTP',
            f'Your OTP to confirm the order is {otp}',
            'noreply@yourshop.com',
            [order.customer.email],
            fail_silently=False,
        )
        return render(request, 'confirm_order.html', {'order': order})

def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'product_detail.html', {'order': order})


def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, 'Order cancelled successfully.')
    return redirect('order_history')
 

def buy_now(request):
    customer_id=request.session.get('customer_id')
    customer=Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if not product_id:
            return HttpResponseBadRequest("Product ID is missing.")

        add_to_cart(request,product_id)

       
        return redirect('order_summary')  
    
    return HttpResponseBadRequest("Invalid request method.")


def edit_profile_view(request):
    if not request.session.get('customer_id'):
        messages.error(request, "Please log in first")
        return redirect('user_login')

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)

    if request.method == "POST":
        if 'otp' in request.POST:
            entered_otp = request.POST.get('otp')
            try:
                customer_otp_entry = customer_otp.objects.get(customer=customer, otp=entered_otp)
            except customer_otp.DoesNotExist:
                messages.error(request, "Invalid OTP. Please try again.")
                return render(request, 'otp_form.html')

            messages.success(request, "OTP verified. You can now edit your profile.")
            return render(request, 'edit_profile.html', {'customer': customer})


        elif 'fname' in request.POST:

            fname = request.POST.get('fname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('pass1')

            customer.fname = fname
            customer.email = email
            customer.Phone = phone
            customer.pass1 = password
            customer.pass2=password
            customer.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('/profile/')

    else:
        otp = str(random.randint(100000, 999999))
        customer_otp.objects.create(customer=customer, otp=otp)

        send_mail(
            'Your OTP for Profile Edit',
            f'Your OTP is {otp}',
            'noreply@yourshop.com',
    
            [customer.email],
            fail_silently=False,
        )
        messages.success(request, 'An OTP has been sent to your email.')
        return render(request, 'otp_verification.html')






    
    
    

  

    

    
    







