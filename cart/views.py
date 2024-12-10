from .carts import Cart
from django.views import generic
from product.models import Product
from .models import Coupon
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404 , redirect , render
from django.contrib import messages

class AddToCart(generic.View):
     def post(self, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        cart = Cart(self.request)
        cart.update(product.id, 1)
        return redirect('cart')

class CartItems(generic.TemplateView):
   template_name = 'cart/cart.html'

   def get(self, request, *args, **kwargs):
      product_id = request.GET.get('product_id', None)
      quantity = request.GET.get('quantity', None)
      clear = request.GET.get('clear', False)
      delivery_option = request.GET.get('delivery_option', None)

      if product_id and quantity:
         product = get_object_or_404(Product, id=product_id)
         if int(quantity) > 0:
            if product.in_stock:
               cart = Cart(request)
               cart.update(int(product_id), int(quantity)) 
               return redirect('cart')
            else:
               messages.warning(request, 'Product is out of stock.')
               return redirect('cart')
         else:
            cart = Cart(request)
            cart.update(int(product_id), int(quantity)) 
            return redirect('cart')
         
      if delivery_option:
         cart = Cart(request)
         cart.set_delivery_option(delivery_option)  
         self.request.session['delivery_option'] = delivery_option
         return redirect('cart')

      
      if clear:
         cart = Cart(request)
         delivery_option = request.session.get('free') 
         cart.clear()
         return redirect('cart')

      return super().get(request, *args, **kwargs)

class AddCoupon(generic.View):
   def post(self, request, *args, **kwargs):
      code = request.POST.get('coupon', None)
      coupon = Coupon.objects.filter(code__iexact=code, active=True)
      cart = Cart(self.request)

      if coupon.exists():
         coupon = coupon.first()
         current_date = datetime.date(timezone.now())
         active_date = coupon.active_date
         expiry_date = coupon.expiry_date
         if current_date > expiry_date:
            messages.warning(self.request, 'Coupon has expired.')
            return redirect('cart')
         if current_date < active_date:
            messages.warning(self.request, 'The coupon is yet to be available')
            return redirect('cart')
         if cart.total() < coupon.required_amount_to_use_coupon:
            messages.warning(request, 'The cart total does not meet the required amount for this coupon.')
            return redirect('cart')

         cart.add_coupon(coupon.id)
         messages.success(request, 'Coupon applied successfully.')
         return redirect('cart')
      else:
         messages.warning(self.request, 'Invalid coupon code.')
         return redirect('cart')
      