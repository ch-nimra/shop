from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from django.contrib.auth.decorators import login_required
from shop.views import user_login
# Create your views here.

# @login_required
@require_POST
def cart_add(request, product_id):
    # print("here")
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if request.user.is_authenticated:
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:cart_detail')
    else:
        return redirect('login')

@login_required
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if cart:
            return redirect('cart:cart_detail')
    return redirect('/')

@login_required
def cart_detail(request):
    cart = Cart(request)
  
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'override': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item ['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products,max_results=4)
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form,
                                                'recommended_products': recommended_products})

