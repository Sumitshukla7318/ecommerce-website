from django.shortcuts import render, redirect
from .models import Admin_register,AdminOTP
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Category, Product,Block
from django.contrib.auth.decorators import login_required
from userapk.models import Customer
from datetime import timedelta,datetime
from django.utils import timezone
import os
import random
from django.core.mail import send_mail
from django.utils import timezone


def admin_panel(request):
    return render(request, "admin_panel.html")

def admin_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        
        admin = Admin_register.objects.create(email=email,password=password,first_name=first_name,last_name=last_name,phone_number=phone_number,address=address
        )
        admin.save()
        return HttpResponseRedirect('/admin_panel/')
    return render(request, 'admin_signup.html')




def admin_login(request):
    if 'admin_email' in request.session:
        return redirect('/admin_panel/') 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Admin_register.objects.get(email=email)
        except Exception as e:
            messages.error(request, 'Admin with this email does not exist.')
            return render(request, 'admin_login.html')

       
        failed_attempt = Block.objects.filter(adminn=admin).first()
        block_time = timedelta(minutes=1)
        # current_time =datetime.now().strftime("%H:%M:%S")
        current_time=timezone.now()

        if failed_attempt and failed_attempt.attempts >= 3:
            last_attempt_time = failed_attempt.last_attempt
            if current_time-last_attempt_time <= block_time:
                messages.error(request, 'You are blocked for 2 minutes due to too many failed login attempts.')
                return render(request, 'admin_login.html')

        if admin.password==password:
           
            if failed_attempt:
                failed_attempt.attempts = 0
                failed_attempt.save()
            request.session['admin_name'] = admin.first_name+admin.last_name
            request.session['admin_email'] = admin.email
            return redirect('/admin_panel/')
        else:
            if failed_attempt:
                failed_attempt.attempts+=1
                failed_attempt.last_attempt=current_time
                failed_attempt.save()
            else:
                Block.objects.create(adminn=admin, attempts=1, last_attempt=current_time)
            messages.error(request, 'Invalid email or password.')

    return render(request, 'admin_login.html')

def admin_logout(request):
    if 'admin_email' in request.session:
        del request.session['admin_email']
    if 'admin_name' in request.session:
        del request.session['admin_name']
    print("rendering admin login")
    return redirect('/admin_panel')


def add_product(request):
    if 'admin_email' not in request.session:
        return redirect('/admin_panel/admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        des = request.POST.get('des')
        image = request.FILES.get('image')
        category = Category.objects.get(id=category_id)
        Product.objects.create(name=name, price=price, category=category, des=des, image=image)
        messages.success(request, 'Product added successfully!')
        return redirect('/admin_panel/')
    categories = Category.objects.all()
    return render(request, 'add_product.html', {'categories': categories})


def add_category(request):
    if 'admin_email' not in request.session:
        return redirect('/admin_panel/admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        des = request.POST.get('des')
        Category.objects.create(name=name, des=des)
        messages.success(request, 'Category added successfully!')
        return redirect('/admin_panel')
    return render(request, 'add_category.html')

def view_product(request):
    if 'admin_email' not in request.session:
        return redirect('/admin_panel/admin_login')
    prods=Product.objects.all()
    return render(request,'view_product.html',{'prods':prods})

def deleteproduct(request,id):
    rec=Product.objects.get(id=id)
    rec.delete()
    os.remove(rec.image.path)
    return redirect('/admin_panel/view_product')

def editproduct(request, id):
    print(id)
    product = Product.objects.get(id=id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id)
        product.des = request.POST.get('des')
        # product.image = request.FILES['image']

        product.save()
        return redirect('view_product') 

    categories = Category.objects.all()
    return render(request, 'update_record.html', {'product': product, 'categories': categories})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            admin = Admin_register.objects.get(email=email)
        except Exception:
            messages.error(request, 'Admin with this email does not exist.')
            return render(request, "forgot_password.html")

        otp = random.randint(100000, 999999)
        AdminOTP.objects.create(admin=admin, otp=str(otp))
        
        send_mail(
            'Your OTP for Password Reset',
            f'Your OTP is {otp}',
            'Sumitshukla7318@gmail.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, 'OTP has been sent to your email.')
        return redirect('reset_password')

    return render(request, "forgot_password.html")

def reset_password(request):
    if request.method=="POST":
        otp=request.POST.get('otp')
        new_password=request.POST.get('new_password')

        try:
            admin_otp=AdminOTP.objects.get(otp=otp)
        except:
            print("exce[t block running]")
            messages.error(request,"Invalid Otp")
            return render(request,"reset_admin_pass.html")
        
        admin=admin_otp.admin
        admin.password=new_password
        admin.save()
        messages.success(request, 'Password has been reset successfully.')
        return redirect('admin_login')
    return render(request,"reset_admin_pass.html")



def view_customer(request):
    rec = Customer.objects.all()
    print(rec)
    
    return render(request, "view_customer.html", {'rec': rec})
