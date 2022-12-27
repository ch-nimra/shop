from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from django.contrib.auth.decorators import login_required
from shop.views import UserLoginView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# @login_required
# @require_POST
class CartAddView(LoginRequiredMixin,View):
    
    def post(self, request, product_id):

        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                cd = form.cleaned_data
                cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        print("here")
        return redirect('cart:cart_detail')

class CartRemoveView(LoginRequiredMixin, View):    
    def post(self,request):
        product_id =  self.request.POST.get('del_id')
        # print('jhassvxdghsh')
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        
        return JsonResponse(data={"status": 204})

    
class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
  
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'override': True})
        coupon_apply_form = CouponApplyForm()
        r = Recommender()
        cart_products = [item['product'] for item in cart]
        # recommended_products = r.suggest_products_for(cart_products, max_results=4)
        return render(request, 'cart/detail.html', {'cart': cart,
                                                    'coupon_apply_form': coupon_apply_form,
                                                    'recommended_products': {}})
        



