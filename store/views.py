from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from . models import *
from . utils import cookieCart, cartData, guestOrder

# Create your views here.

#This will help us view product name, image, total prices, tota items, items we have, to store page

def store(request):

	#Qurey Data for user at store page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	#Qurey Data for user at cart page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
    
    #Qurey Data for user at checkout page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

	
def updateItem(request):

	#UPDATE Items at cart page
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	#If we click n numbers of times on "Add to cart" n numbers of quantity will be displayed
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	#This will save the item to cart
	orderItem.save()

	#If quantity is LESS THAN ZERO, it will delete that item from the cart page
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item is updated to cart', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	#If user is authenticated then customer is created  
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	#If user is not authenticated then customer is created as a guest user
	else:
		customer, order = guestOrder(request, data)


	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)
	#After making payment alert message pop-up "Payment complete!" in console panel	
	return JsonResponse('Payment complete!', safe=False)

def about(request):

	#Qurey Data for user at ABOUT US page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/about.html', context)

def contact(request):

	#Qurey Data for user at CONTACT US page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/contact.html', context)

def terms(request):
	
	#Qurey Data for user at T&C page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/t&c.html', context)

def policy(request):

	#Qurey Data for user at POLICY page
	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/policy.html', context)