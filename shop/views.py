from cart.forms import CartAddProductForm
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm
from .models import Category, Product
from .recommender import Recommender
from django.contrib.auth.decorators import login_required

# Create your views here.


def user_login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:          
                
            if user.is_active:
                login(request, user)
                return redirect ('shop:product_list')
                
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:  
         
        if request.user.is_authenticated:

        #     # login(request,user) 
            return redirect ('shop:product_list')
        
        form = LoginForm()
        return render(request, 'shop/account/login.html', {'form': form})
    

def user_logout(request): 
    logout(request)
    return redirect('login')  
    # return render(request, 'shop/registration/logged_out.html')      

def product_list(request, category_slug=None):
    category =  None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language =  request.LANGUAGE_CODE
        category = get_object_or_404(Category, 
                                    translations__language_code = language,
                                    translations__slug=category_slug)
        products = products.filter(category=category)

    
    return render(request, 'shop/product/list.html', {'category': category,
                                                        'categories': categories,
                                                        'products': products })

def product_detail(request, id, slug):
    
    language = request.LANGUAGE_CODE
     
    # products = Product.objects.filter(id=id,
    #                             translations__language_code = language,
    #                             translations__slug=slug,
    #                             available=True)

    product = []
    try:
        product= get_object_or_404(Product, 
                                    id=id,
                                    translations__language_code = language,
                                    translations__slug=slug,
                                    available=True)
    except:
        print("No object found...")
    
    cart_product_form = CartAddProductForm()

    r= Recommender()
    recommended_products= r.suggest_products_for([product], 4)
    return render (request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form,
                                                        'recommended_products': recommended_products})


