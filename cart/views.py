from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import Cart, CartItems
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

        # check if user has cart
        if not Cart.objects.filter(user=self.request.user).exists():
            cart= Cart.objects.create(user=self.request.user)
        else: 
            cart= Cart.objects.get(user=self.request.user)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            # check if the product is in cart
            if not CartItems.objects.filter(product_id=product_id).exists():
                cartitem= CartItems.objects.create(product_id=product_id, qty=request.POST.get('quantity'), cart=cart)
            else: 
                cartitem= CartItems.objects.get(product_id=product_id)
                cartitem.qty = cartitem.qty + request.POST.get('quantity')
                cartitem.save()

            cd = form.cleaned_data
        print("here")
        return redirect('cart:cart_detail')

class CartRemoveView(LoginRequiredMixin, View):    
    def post(self,request):
        product_id =  self.request.POST.get('del_id')
        # print('jhassvxdghsh')
        cart = Cart()
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
        



