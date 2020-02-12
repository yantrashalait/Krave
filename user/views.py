from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from .forms import ValidatingPasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import UserProfile
from django.contrib.auth import get_user_model
from core.models import Order
from django.db.models import Q

User = get_user_model()


@login_required
def userprofile(request, *args, **kwargs):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    past_orders = Order.objects.filter(~Q(status=0), user=request.user)
    current_orders = Order.objects.filter(status=0, user=request.user)
    if request.method == "POST":
        if 'password-change' in request.POST:
            password_form = ValidatingPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect(reverse_lazy('user:profile'))
            else:
                return render(request, 'core/user-profile.html', {'password_error': 1, 'profile': user_profile, 'password_form': password_form, 'password-reset': 1, 'order_history': past_orders, 'current_orders': current_orders})
    else:
        password_form = ValidatingPasswordChangeForm(request.user)

    return render(request, 'core/user-profile.html', {'profile': user_profile, 'password_form': password_form, 'order_history': past_orders, 'current_orders': current_orders})


def edit_profile(request, *args, **kwargs):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        zip = request.POST.get('zip')
        image = request.POST.get('image')
        print(request.POST)

        user = User.objects.get(id=request.user.id)
        if first_name != user.first_name:
            user.first_name = first_name

        if last_name != user.last_name:
            user.last_name = last_name

        user.save()

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.contact = contact
        user_profile.address = address
        user_profile.zip_code = zip
        if image != '':
            user_profile.image = image
        user_profile.save()

        return redirect(reverse_lazy('user:profile'))
