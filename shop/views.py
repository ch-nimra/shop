from cart.forms import CartAddProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import LoginForm, SearchForm
from .models import Category, Product
from .recommender import Recommender

# Create your views here.


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
        #     # login(request,user) 
            return redirect ('shop:product_list')
        
        form = LoginForm()
        return render(request, 'shop/account/login.html', {'form': form})
    
    def post(self,request):
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


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class ProductListView(View):
    def get(self,request, category_slug=None):
        category =  None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        paginator = Paginator(products,3)
        page_number = request.GET.get('page')
        product_data_final = paginator.get_page(page_number)

        
        

        if category_slug:   
            language =  request.LANGUAGE_CODE
            category = get_object_or_404(Category, 
                                        translations__language_code = language,
                                        translations__slug=category_slug)
            product_data_final = product_data_final.filter(category=category)

       

        search_param = request.GET.get('q',None)
        if search_param:
            product_data_final = products.filter(translations__name__icontains=search_param)
        
        return render(request, 'shop/product/list.html', {'category': category,
                                                            'categories': categories,
                                                            # 'products': products,
                                                            'product_data': product_data_final})

class ProductDetailView(View):
    def get(self, request, id, slug):
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




