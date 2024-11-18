from django.shortcuts import render,redirect,get_object_or_404
from account.models import *
from django.contrib import messages
import http.client
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime 

# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def adduser(request):
    username = "Admin"
    password = "password"
    user, created = CustomUser.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        return HttpResponse("User created successfully.")
    else:
        return HttpResponse("User already exists.")
@login_required(login_url='login')
@never_cache

def home(request):
    farmer = CustomUser.objects.filter(category="Farmer").count()
    products=Products.objects.all().count()
    return render(request, 'index.html',{'farmer':farmer,'products':products})

@login_required(login_url='login')
@never_cache
def add_farmer(request):
    if request.method == "POST":
        username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = "qwerty"
        category = request.POST.get('category')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        user = CustomUser(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            category=category,
            phone=phone,
            gender=gender
        )
        user.set_password(password)  # Hash the password before saving
        user.save()
        return redirect('farmer_success')  
    return render(request,'add_farmer.html')

@login_required(login_url='login')
@never_cache
def edit_farmer(request, id):
    farmer1 = CustomUser.objects.filter(id=id)
    
    if request.method == "POST":
        username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = "qwerty"
        category = request.POST.get('category')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        id1 = request.POST.get('id1')
        
        far = CustomUser.objects.get(id=id1)
        
        far.username = username
        far.first_name = first_name
        far.last_name = last_name
        far.email = email
        far.category = category
        far.phone = phone
        far.gender = gender
        
        far.save()
        return redirect('farmer_success_update')
        
    return render(request, 'edit_farmer.html', {'farmer1': farmer1})

@login_required(login_url='login')
@never_cache
def delete_farmer(request, id):
    farmer = get_object_or_404(CustomUser, id=id)
    
    if request.method == "POST":
        farmer.delete()
        messages.success(request, "The farmer has been successfully deleted.")
        return redirect('farmer_list')  # Adjust this to the name of your list view or success page
    
    return render(request, 'confirm_delete.html', {'farmer': farmer})

@login_required(login_url='login')
@never_cache
def farmer_success(request):
    return render(request,'farmer_success.html')

@login_required(login_url='login')
@never_cache
def farmer_success_update(request):
    return render(request,'farmer_success_update.html')

def milk_success(request):
    return render(request,'milk_success.html')

def report_success(request):
    return render(request,'report_success.html')

@login_required(login_url='login')
@never_cache
def user_list(request):
    users = CustomUser.objects.filter(category='farmer')
    return render(request, 'farmer_list.html', {'users': users})

@login_required(login_url='login')
@never_cache
def report2(request):
    users = CustomUser.objects.filter(category='farmer')
    return render(request, 'report2.html', {'users': users})

@login_required(login_url='login')
@never_cache
def add_milk(request):
    products=Products.objects.filter(quantities__gte=1)
    users1=CustomUser.objects.filter(category='farmer')
    price=MilkPrice.objects.all()
    if request.method == 'POST':
        customuser = request.POST.get('category')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')
        want_product = request.POST.get('want_product')
        product_id = request.POST.get('product')
        product_quantity = request.POST.get('product_quantity')
        milk_q=request.POST.get('milk_q')
        product_amount=0
        price_milk=float(quantity)*float(milk_q)
        if want_product:
            pro_price=Products.objects.get(id=product_id)
            price1=pro_price.price_unit
            product_amount=float(price1)*float(product_quantity)

        user_object1 = get_object_or_404(CustomUser, id=customuser)
        user=CustomUser.objects.get(id=customuser)
        phone=user.phone
        names1=user.first_name + user.last_name
        phone1="25"+phone
        print(phone1)
        print(phone)
        # Create a new Milk instance and save it
        milk = Milk.objects.create(
            customuser_id=customuser,
            quantity=quantity,
            price=price_milk,
            date1=date,
            product_amount=product_amount
        )
        mesage="Munyamuryango mwiza "+names1+ " Amata yawe yakiriwe neza, hakiriwe litiro "+quantity+" kuwa "+date+" Murakoze!"
        send_sms(phone1,mesage)
        messages.success(request, 'Record saved successfully!')
        return redirect('milk_success')   

    return render(request,'record_milk.html',{'products':products,'user1':users1,'price':price})
@login_required(login_url='login')
@never_cache
def milk_price(request):
    price=MilkPrice.objects.all()
    return render(request,'milk_price.html',{'price':price})

@login_required(login_url='login')
@never_cache
def milk_list(request):
    milk=Milk.objects.all()
    return render(request,'milk_list.html',{'milk':milk})

@login_required(login_url='login')
@never_cache
def report(request):
    date_filter = request.GET.get('date')
    farmer_filter = request.GET.get('farmer')

    milk_data = Milk.objects.all()

    if date_filter:
        date_filter = datetime.strptime(date_filter, '%Y-%m-%d')
        milk_data = milk_data.filter(date1__date=date_filter)
    if farmer_filter:
        milk_data = milk_data.filter(customuser_id=farmer_filter)

    farmers = CustomUser.objects.all()

    if 'download' in request.GET:
        filtered_milk_data = milk_data
        return generate_pdf_response(request, filtered_milk_data)

    return render(request, 'report1.html', {'milk': milk_data, 'farmers': farmers})

def generate_pdf_response(request, filtered_milk_data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="milk_report.pdf"'

    generate_pdf(response, filtered_milk_data)

    return response

def generate_pdf(response, filtered_milk_data):
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    table_data = [['Date', 'Farmer Name', 'Quantity', 'Amount', 'Product Amount']]
    for milk in filtered_milk_data:
        table_data.append([
            str(milk.date1),
            f"{milk.customuser.first_name} {milk.customuser.last_name}",
            f"{milk.quantity}L",
            f"{milk.price}",
            f"{milk.product_amount}"
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))

    elements.append(table)
    doc.build(elements)
@login_required(login_url='login')
@never_cache
def add_products(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantities = request.POST.get('quantities')
        price_unit = request.POST.get('price_unit')

        # Create a new product instance and save it
        product = Products(product_name=product_name, quantities=quantities, price_unit=price_unit)
        product.save()

        # Redirect to the same page with a success flag
        return redirect('/add_products?success=True')

    # Check if the success flag is in the request
    success = 'success' in request.GET

    return render(request, 'add_product.html', {'success': success})

@login_required(login_url='login')
@never_cache
def request_product(request):
    products = Products.objects.all()
    users = CustomUser.objects.filter(category="farmer")
    if request.method == "POST":
        farmer_id = request.POST.get('farmer')
        product_id = request.POST.get('product_name')
        quantity = float(request.POST.get('quantities'))
        farmer = CustomUser.objects.get(id=farmer_id)
        product = Products.objects.get(id=product_id)
        ProductRequest.objects.create(
            farmer=farmer,
            product=product,
            quantity=quantity,
            date_requested=datetime.date.today()
        )
        return redirect('product_success')
    return render(request, 'request_product.html', {'products': products, 'users': users})

def product_success(request):
    return render(request, 'product_success.html')
@login_required(login_url='login')
@never_cache
def monthly_payment_report(request):
    if request.method == 'POST':
        user_id = request.POST.get('farmer')
        user = get_object_or_404(CustomUser, id=user_id)
        month = datetime.date.today().replace(day=1)  # Assuming current month
        payment_record = MonthlyPayment.calculate_for_user(user, month)
        return render(request, 'monthly_payment_report.html', {'payment_record': payment_record, 'selected_user': user})
    else:
        users = CustomUser.objects.filter(category='farmer')
        return render(request, 'select_user.html', {'users': users})

@login_required(login_url='login')
@never_cache
def send_report(request):
    if request.method == 'POST':
        user_id = request.POST.get('id1')
        phone=request.POST.get('phone')
        income=request.POST.get('income')
        net=request.POST.get('net')
        deduct=request.POST.get('deduct')
        
        message1="raporo yawe,\n amata wazanye yose:"+income+"Rwf\n ibyo watwaye:"+deduct+"Rwf\n ayo wishyurwa yose:"+net+"Rwf\n Murakoze."
        send_sms(phone,message1)
        messages.success(request, 'Report Sended!')
        return redirect('report_success') 
    
@login_required(login_url='login')
@never_cache
def edit_products(request,id):
    product=Products.objects.filter(id=id)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantities = request.POST.get('quantities')
        price_unit = request.POST.get('price_unit')
        id1=request.POST.get('id1')
        print("iddd",id1)
        # Create a new product instance and save it
        product = Products.objects.get(id=id1)
        product.product_name=product_name
        product.quantities=quantities
        product.price_unit=price_unit
        product.save()

        # Redirect to the same page with a success flag
        return redirect('/edit_products/1?success=True')

    # Check if the success flag is in the request
    success = 'success' in request.GET

    return render(request, 'edit_product.html', {'success': success,'product':product})
@login_required(login_url='login')
@never_cache
def delete_product(request, id):
    product = get_object_or_404(Products, id=id)
    
    if request.method == "POST":
        product.delete()
        messages.success(request, "The product has been successfully deleted.")
        return redirect('product_list')  # Adjust this to the name of your product list view or success page
    
    return render(request, 'confirm_delete.html', {'product': product})

@login_required(login_url='login')
@never_cache
def change_price(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        

        # Create a new product instance and save it
        MilkPrice.objects.all().delete()
        price = MilkPrice(price_unit=amount)
        price.save()

        # Redirect to the same page with a success flag
        return redirect('/change_price?success=True')

    # Check if the success flag is in the request
    success = 'success' in request.GET

    return render(request, 'change_price.html', {'success': success})
@login_required(login_url='login')
@never_cache
def product_list(request):
    products = Products.objects.all()
    for product in products:
        product.total_price = product.price_unit * product.quantities
    return render(request, 'product_list.html', {'products': products})



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/home')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    return render(request, 'login.html')

def signup(request):
    return render(request,'signup.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def send_sms(phone, message):
    conn = http.client.HTTPSConnection("mmg1mw.api.infobip.com")
    payload = json.dumps({
        "messages": [
            {
                "destinations": [{"to": phone}],
                "from": "ServiceSMS",
                "text": message
            }
        ]
    })
    headers = {
        'Authorization': 'App 1219c9ff758ebbf48554a8d2a0e9448a-abfb332c-9cf6-401d-9b8f-37f121958fc2',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))