from django.contrib.auth.models import Group, Permission
from userrole.models import UserRole
from .models import UserProfile
from social_django.models import UserSocialAuth
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from urllib.request import urlretrieve
from urllib.parse import urlparse
from django.core.files import File
from django.contrib.auth import get_user_model
from core.models import FoodCart

User = get_user_model()

# check if the email already exists for the user trying to login through gmail
def email_validate(strategy, backend, uid, user, response, *args, **kwargs):
    email = response.get('email')

    # check if given email is in use
    django_user_exists = User.objects.filter(email=email).exists()
    u = User.objects.get(email=email)
    social_auth_user_exists = UserSocialAuth.objects.filter(user=u).exists()

    # user is not logged in, social profile with given uid doesn't exist
    # and email is in use
    if django_user_exists and not social_auth_user_exists:
        return {
            'user':u
        }
    else:
        return {
            'user':user
        }


# create a role as unassigned for the logged in user if the role is not created
def create_role(backend, uid, user, response, social=None, *args, **kwargs):
    email = response.get('email')

    if user and not social:
        social = backend.strategy.storage.user.create_social_auth(user, uid, backend.name)

    u = User.objects.get(email=email)

    try:
        if u.groups.filter(name="support").exists() \
            or u.groups.filter(name="restaurant-owner").exists() \
            or u.groups.filter(name="delivery") \
            or u.groups.filter(name="super-admin").exists():
            pass
        else:
            group = Group.objects.get(name="customer")
            u.is_customer = True
            u.save()
            userrole = UserRole.objects.filter(user=u)
            if not u.groups.filter(name="customer").exists():
                u.groups.add(group)
            if not userrole:
                UserRole.objects.create(user=u, group=group)
    except:
        group = Group.objects.get(name="customer")
        userrole = UserRole.objects.filter(user=u)
        u.is_customer = True
        u.save()
        if not userrole:
            UserRole.objects.create(user=u, group=group)

    return {
        'social':social,
        'user':user,
    }


# create a profile for the logged in user if profile doesnot exist
def create_profile(strategy, backend, uid, user, response, social=None, *args, **kwargs):
    email = response.get('email')
    request = strategy.request
    redirect = strategy.redirect

    u = User.objects.get(email=email)
    try:
        if u.user_roles.group.name == 'restaurant-owner':
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            restaurant_id = u.user_roles.restaurant.id
            return HttpResponseRedirect(reverse('restaurant:dashboard', kwargs={'rest_id': restaurant_id}))
    except:
        pass

    if FoodCart.objects.filter(session_key=strategy.session.session_key, user=None, checked_out=False).exists():
        FoodCart.objects.filter(session_key=strategy.session.session_key, user=None, checked_out=False).update(user=u)

    try:
        profile = UserProfile.objects.get(user=u)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect(reverse('core:dashboard'))

    except UserProfile.DoesNotExist:
        user_name = response.get('name')
        user_name = user_name.split(' ')
        u.first_name = user_name[0]
        u.last_name = user_name[1]
        u.save()

        profile = UserProfile.objects.create(user=u)


        #save profile picture from google
        picture = response.get('picture')
        name = urlparse(picture).path.split('/')[-1]
        content = urlretrieve(picture)
        profile.image.save(name, File(open(content[0], 'rb')), save=True)

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect(reverse_lazy('user:profile'))
