from django.utils.deprecation import MiddlewareMixin

class AddUserRolesToContextMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            request.user_roles = request.user.groups.values_list('name', flat=True)
            print("User roles:", request.user_roles)  # Mensaje de depuración
        else:
            request.user_roles = []
        return None
