from .models import FoodCart, Order

def get_header_notifs(request):
    if request.user.is_authenticated:
        user = request.user
        cart = FoodCart.objects.filter(user=request.user, checked_out=False)
        cart_count = FoodCart.objects.filter(user=request.user, checked_out=False).count()
        return {'cart': cart, 'cart_count': cart_count}
    else:
        return {'message': 'not authenticated'}
