# -*- coding: utf-8 -*-
from .models import AppPer
from django.http  import HttpResponse

#
def access_check(view_func):

def escape_exempt(view_func):
    """
    转义豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
