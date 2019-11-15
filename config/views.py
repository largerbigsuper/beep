from django.shortcuts import redirect


def index(request):
    return redirect(request._current_scheme_host + '/beepui/')
