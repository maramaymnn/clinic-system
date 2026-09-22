from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='/login/')
        def wrapper(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return redirect('dashboard')

        return wrapper

    return decorator
