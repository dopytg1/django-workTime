from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

class CompanyRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_company:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def company_allowed():
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.is_company:
				return view_func(request, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator


class MemberRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_member:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def member_allowed():
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.is_member:
				return view_func(request, *args, **kwargs)
			else:
				raise PermissionDenied
		return wrapper_func
	return decorator