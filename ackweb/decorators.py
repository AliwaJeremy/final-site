from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('userhome')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group =  request.user.groups.all()[0].name 
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponse('You are not aothorised to view this page')
        return wrapper_func
    return decorator


    #admin only
def superuser_only(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group =  request.user.groups.all()[0].name 
            
            if group == 'admin':
                return redirect('userhome')

            if group == 'user':
                return redirect('userhome')

            if group == 'superuser': 
                return view_func(request, *args, **kwargs)
            
            else:
                return redirect('userhome')


        return wrapper_func
   

