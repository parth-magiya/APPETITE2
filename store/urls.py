from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('about/', views.about, name="about"),
	path('contact/', views.contact, name="contact"),
	path('terms&conditions/', views.terms, name="t&c"),
	path('privacy-policy/', views.policy, name="policy"),
]