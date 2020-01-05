from userrole.models import UserRole as Role
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.deprecation import MiddlewareMixin


def clear_roles(request):
    request.__class__.role = None
    request.__class__.restaurant = None
    return request


class RoleMiddleware(MiddlewareMixin):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
        ]

    def process_request(self, request):
        if request.META.get('HTTP_AUTHORIZATION'):
            token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
            try:
                if request.user.is_anonymous():
                    request.user = Token.objects.get(key=token_key).user
            except:
                pass

        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()

        if not request.user.is_anonymous:
            role = None
            if request.session.get('role'):
                try:
                    role = Role.objects.select_related('group', 'restaurant').get(pk=request.session.get('role'), user=request.user)
                except Role.DoesNotExist:
                    pass
            if not role:
                roles = Role.objects.filter(user=request.user).select_related('group', 'restaurant')
                if roles:
                    role = roles[0]
                    request.session['role'] = role.id
                
            if role:
                request.__class__.role = role
                request.__class__.restaurant = role.restaurant
            
            else:
                request = clear_roles(request)
                logout(request)
                return render(request, '403.html')
        else:
            request = clear_roles(request)