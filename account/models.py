from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):   # Add your custom fields
    
   
    category = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    gender =models.CharField(max_length=50)
    
    
class Milk(models.Model):
    customuser=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity=models.CharField(max_length=250)
    price=models.CharField(max_length=50)
    date1=models.DateTimeField(auto_now_add=True)    
    product_amount=models.CharField(max_length=250)
    
class MilkPrice(models.Model):
    price_unit=models.FloatField()  
    
class Products(models.Model):
    product_name=models.CharField(max_length=50)
    quantities = models.FloatField()  
    price_unit = models.FloatField() 
    
class ProductRequest(models.Model):
    farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date_requested = models.DateField()

    @property
    def total_price(self):
        return self.quantity * self.product.price_unit



class MonthlyPayment(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.DateField()
    total_milk_income = models.FloatField()
    total_product_deduction = models.FloatField()
    net_payment = models.FloatField()

    @staticmethod
    def calculate_for_user(user, month):
        # Calculate total income from milk
        milk_records = Milk.objects.filter(customuser=user, date1__month=month.month, date1__year=month.year)
        total_milk_income = sum(float(record.price) for record in milk_records)

        # Calculate total deduction from product requests
        product_requests = ProductRequest.objects.filter(farmer=user, date_requested__month=month.month, date_requested__year=month.year)
        total_product_deduction = sum(float(request.total_price) for request in product_requests)

        # Calculate net payment
        net_payment = total_milk_income - total_product_deduction

        # Create or update the monthly payment record
        payment_record, created = MonthlyPayment.objects.get_or_create(customuser=user, month=month, defaults={
            'total_milk_income': total_milk_income,
            'total_product_deduction': total_product_deduction,
            'net_payment': net_payment,
        })

        if not created:
            payment_record.total_milk_income = total_milk_income
            payment_record.total_product_deduction = total_product_deduction
            payment_record.net_payment = net_payment
            payment_record.save()

        return payment_record
class Reports(models.Model):
    report_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20)
    report_date = models.DateField()
    report_data = models.TextField()
    
class Payments(models.Model):
    customuser=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount=models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    pay_date=models.DateField()
    product_id=models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    
    