from django.http import JsonResponse
from .models import Token

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            auth_token = request.headers.get('Authorization')
            try:
                token = Token.objects.get(key=auth_token)
                if token.is_expired():
                    return JsonResponse({'error': 'Token expired'}, status=401)
                request.user = token.user
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = None

        response = self.get_response(request)
        return response



