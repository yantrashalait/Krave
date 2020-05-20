from .models import FoodCart, Order, Notification

def get_header_notifs(request):
    if request.user.is_authenticated:
        user = request.user
        cart = FoodCart.objects.filter(user=request.user, checked_out=False)
        cart_count = FoodCart.objects.filter(user=request.user, checked_out=False).count()
        notification = Notification.objects.filter(destination=request.user).order_by('-date_created')
        notification_count = Notification.objects.filter(destination=request.user).count()
        return {'cart': cart, 'cart_count': cart_count, 'notification': notification, 'notification_count': notification_count}
    else:
        return {'message': 'not authenticated'}
