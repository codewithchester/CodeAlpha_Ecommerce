from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def checkout(request):
    """Handle order processing"""
    cart = request.session.get('cart', {})
    
    # If cart is empty, go back to store
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('product_list')
    
    if request.method == 'POST':
        # Get customer info from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Create the order
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
        )
        
        # Add each cart item to the order
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=int(product_id))
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=quantity,
            )
        
        # Clear the cart
        request.session['cart'] = {}
        
        messages.success(request, f'Order #{order.id} placed successfully! Thank you for your purchase.')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'store/checkout.html', {'cart': cart})


def order_confirmation(request, order_id):
    """Show order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})