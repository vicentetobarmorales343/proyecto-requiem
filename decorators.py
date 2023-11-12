from django.shortcuts import redirect


def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'login_status' not in request.session or not request.session['login_status']:
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def redirect_if_logged_in(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'login_status' in request.session and request.session['login_status']:
            return redirect('home')  # or wherever you want to redirect
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def role_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'role' in request.session and request.session['role'] == 3:
            return redirect('home')  # or wherever you want to redirect
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'role' in request.session and request.session['role'] == 2:
            return redirect('home')  # or wherever you want to redirect
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
