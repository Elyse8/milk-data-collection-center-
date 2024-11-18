from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home,name='home'),
    path('',views.login,name='login'),
    path('adduser1/',views.adduser,name='adduser'),
    path('add_farmer/',views.add_farmer,name='add_farmer'),
    path('edit_farmer/<int:id>',views.edit_farmer,name='edit_farmer'),
    path('farmer_success/',views.farmer_success,name='farmer_success'),
    path('farmer_success_update/',views.farmer_success_update,name='farmer_success_update'),
    path('milk_success/',views.milk_success,name='milk_success'),
    path('report_success/',views.report_success,name='report_success'),
    path('send_report/',views.send_report,name="send_report"),
    path('farmers/', views.user_list, name='farmer_list'),
    path('delete_farmer/<int:id>/', views.delete_farmer, name='delete_farmer'),
    path('record_milk/',views.add_milk,name='record_milk'),
    path('add_products/',views.add_products,name='add_products'),
    path('request_products/',views.request_product,name='request_products'),
    path('edit_products/<int:id>',views.edit_products,name='edit_products'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('product_list/',views.product_list,name='product_list'),
    path('milk_price/',views.milk_price,name='milk_price'),
    path('change_price/',views.change_price,name='change_price'),
    path('milk_list/',views.milk_list,name='milk_list'),
    path('logout/', views.logout, name='logout'),
    path('report1/',views.report,name='report1'),
    path('signup/',views.signup,name='signup'),
    path('report2/',views.report2,name='report2'),
    path('monthly_payment_report/', views.monthly_payment_report, name='monthly_payment_report'),
    path('product_success',views.product_success,name='product_success')
    
    

]