from django.core.exceptions import PermissionDenied

def if_user_is_employer(function):

    def wrap(request, *args, **kwargs):
        if request.user.is_employer:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
    return wrap

def if_user_is_employee(function):

    def wrap(request, *args, **kwargs):
        if not request.user.is_employer:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
    return wrap
