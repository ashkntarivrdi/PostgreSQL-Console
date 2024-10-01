from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Token
from testdb.models import App
from django.utils import timezone
import json

@csrf_exempt
def signup_app(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken'}, status=400)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Missing username or password'}, status=400)

@csrf_exempt
def login_app(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token = Token.generate_token(user)
            return JsonResponse({'token': token.key}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
