from datetime import datetime
import logging
from django.shortcuts import get_object_or_404, render, redirect
import stripe
from django.core import serializers

from phoneproject import settings
from .models import CartItem, Product,Category,Order,OrderProduct
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


# Create your views here.
def storehome(request):
    return render(request, 'store/storehome.html', {'title': 'Next Gen Phone Shop'})


# This view return 'aboutus.html’ files.
def aboutus(request):
    return render(request, 'store/aboutus.html', {'title': 'About us'})

def reviews(request):
    return render(request, 'store/reviews.html', {'title': 'Customer Reviews'})


def shop(request, category = None):
    if category:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category=category)
        return render(request, 'store/shop.html', {'products': products, 'category' : category, 'title': category})
    else:
        products = Product.objects.all()
        return render(request, 'store/shop.html', {'products': products, 'category': 'all', 'title': 'All Phones' })
    
@csrf_exempt 
def create_category(request):
    if request.method == 'POST':
        category = json.loads(request.body)
        if('name' in category.keys()):
          if(len(category['name'].strip()) > 0):
            if(len(category['name']) < 11):
                Category.objects.create(name=category['name'])
                return HttpResponse("Successfully Category Created", status=200)
            else:
              return HttpResponse("Name length should be less than 10", status=400)   
          else:
              return HttpResponse("Name can not be null", status=400) 
        else:
          return HttpResponse("Name Required", status=400) 
        
    return HttpResponse("Error in Request Type", status=500)

@csrf_exempt 
def create_product(request):
    if request.method == 'POST':
        product = json.loads(request.body)
        if('name' in product.keys() and 'price' in product.keys() and 'category' in product.keys()):
          if(len(product['name'].strip()) > 0):
            if(product['price'] > 0):
                category = Category.objects.get(name=product['category'])
                if(category):
                    Product.objects.create(name=product['name'], price=product['price'],
                                           category=category)
                    return HttpResponse("Successfully Product Created", status=200)
                else:
                    return HttpResponse("Category Not Found", status=404)
            else:
              return HttpResponse("Price can not be negative", status=400)   
          else:
              return HttpResponse("Name can not be null", status=400) 
        else:
          return HttpResponse("Name, Price, Category Required", status=400) 
        
    return HttpResponse("Error in Request Type", status=500)

def get_categories(request):
    data = Category.objects.all().values()
    categories = json.dumps(list(data))
    return HttpResponse(categories, status=200)

def get_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return HttpResponse(category, status=200)

@csrf_exempt 
def delete_category(request, category_id):
    if request.method == 'DELETE':
        try:
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return HttpResponse("Successfully Deleted", status=200)
        except Category.DoesNotExist:
            return HttpResponse("Not Found", status=404)
    return HttpResponse("Error in Request Type", status=500)

@csrf_exempt 
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'PUT':
        new_category = json.loads(request.body)
        if('name' in new_category.keys()):
              if(len(new_category['name'].strip()) > 0):
                if(len(new_category['name']) < 11):
                    category.name = new_category['name']
                    category.save()
                    return HttpResponse("Successfully Category Updated", status=200)
                else:
                     return HttpResponse("Name length should be less than 10", status=400)   
              else:
                    return HttpResponse("Name can not be null", status=400) 
        else:
          return HttpResponse("Name Required", status=400) 
    return HttpResponse("Error in Request Type", status=500)

def product(request, product_id):
    product = get_object_or_404(Product , id=product_id)
    return HttpResponse(product, status=200)

def products(request):
    products = serializers.serialize('json', Product.objects.all())
    return HttpResponse(products, status=200)

@csrf_exempt 
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return HttpResponse("Successfully Deleted", status=200)
        except Product.DoesNotExist:
            return HttpResponse("Not Found", status=404)
    return HttpResponse("Error in Request Type", status=500)
#Views for Cartitems management

from django.contrib.auth.decorators import login_required
def add_to_cart(request, product_id):
    if request.user :
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop')

@login_required(login_url='login_user')
def view_cart(request):
    if request.user.is_anonymous:
        pass
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.sale_price * item.quantity for item in cart_items if item.purchase)

        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Shopping Cart'})

from django.contrib.auth.decorators import login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def update_purchase(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item_id = request.POST.get('id')
        purchase_value = request.POST.get('purchase') == 'true'  # Convert to boolean

        try:
            item = CartItem.objects.get(id=item_id)
            item.purchase = purchase_value  # Update the purchase field
            item.save()

            # Recalculate the total price for selected items only
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.sale_price * item.quantity for item in cart_items if item.purchase)

            # Make sure total_price is a number
            total_price = round(total_price, 2)

            # Return calculated total price
            return JsonResponse({'total_price': total_price})
        
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@transaction.atomic
def create_order(request, orderid=None):
    if request.user.is_authenticated:
        try:        
            # If no orderid, create a new order
            new_order = Order.objects.create(customer=request.user, date=datetime.now().date())
            new_order.save()
            
            cart_items_purchase = CartItem.objects.filter(user=request.user, purchase=True)
            if cart_items_purchase:
                for item in cart_items_purchase:
                    product = Product.objects.get(id=item.product_id)
                    soldprice = product.sale_price
                    orderproduct = OrderProduct.objects.create(product=item.product, order=new_order)
                    orderproduct.quantity = item.quantity
                    orderproduct.soldprice = soldprice
                    orderproduct.save()
                    item.delete()

            order_items = OrderProduct.objects.filter(order_id=new_order.id)
            total_price = sum(item.soldprice * item.quantity for item in order_items)
            new_order.total = total_price
            new_order.status = "unpaid"
            new_order.save()

            return redirect('order_details', order_id=new_order.id)

        except Exception as e:
            print("Error creating order occurred:", e)
            return redirect('view_cart')

@transaction.atomic
def pay_order(request, orderid):
    if request.user.is_authenticated:
        try:
            # If orderid is provided, fetch the existing order
            if orderid:
                order_items = OrderProduct.objects.filter(order_id=orderid)
                total_price = sum(item.soldprice * item.quantity for item in order_items)
                return render(request, 'store/order.html', {
                    'order_items': order_items,
                    'total_price': total_price,
                    'title': 'Order Preview',
                    'orderid': orderid.id,
                    'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
                })
        except Exception as e:
            print("Error displaying order occurred:", e)
            return redirect('view_cart')


@transaction.atomic
def delete_order(request, order_id):
    if request.user.is_authenticated:
        try:
            order= Order.objects.get(id=order_id)
    
            order_items_delete = OrderProduct.objects.filter(order_id = order.id)
            if order_items_delete:
                for item in order_items_delete:
                    item.delete()       
        
            order.delete()
            messages.success(request,  f"Your Order {order_id} deleted. Please create a new order...")
            return redirect('view_cart')

        except Exception as e:
            messages.error(request,  f"Your Order {order_id} could not delete. Please contact support center...")
            return redirect('view_cart') 


@login_required(login_url='login_user')
def order_list(request):
    try:
        # Get the selected filter status from the request
        status_filter = request.GET.get('status', None)  # Default to None if no filter is selected

        # Base query to get orders by the logged-in user
        orderlist = Order.objects.filter(customer=request.user)

        # Apply filter based on selected status if applicable
        if status_filter:
            if status_filter == 'paid':
                orderlist = orderlist.filter(status=True)  # Assuming 'True' means 'paid'
            elif status_filter == 'unpaid':
                orderlist = orderlist.filter(status=False)  # Assuming 'False' means 'unpaid'
            elif status_filter == 'delivered':
                orderlist = orderlist.filter(status='delivered')  # Example if status is a string
            elif status_filter == 'deleted':
                orderlist = orderlist.filter(status='deleted')  # Example for 'deleted'

        return render(request, 'store/order_list.html', {'orderlist': orderlist, 'title': "My Orders", 'status_filter': status_filter})
    except:
        messages.error(request, "Orders not found.")
        return redirect('welcome')


@login_required(login_url='login_user')
def order_details(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order_products = order.orderproduct_set.select_related('product')
        return render(request, 'store/order_details.html', {
            'order': order,
            'order_products': order_products,
            'title': "Order Details",
        })
    else:
        messages.error(request, "The order not found.")
        return redirect('welcome')
