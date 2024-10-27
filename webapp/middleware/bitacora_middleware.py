import logging
from webapp.models import Bitacora

logger = logging.getLogger(__name__)

class BitacoraMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request Method: {request.method}, Path: {request.path}")
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            print("User is authenticated")
            action = f"{request.method} {request.path}"
            Bitacora.objects.create(
                user=request.user,
                action=action,
                path=request.path,
                method=request.method
            )
        else:
            print("User is not authenticated")
        
        return response
