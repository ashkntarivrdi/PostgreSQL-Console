from kubernetes import client, config
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import App
from postgresTest import settings
from .kubeclient import *
import json

@csrf_exempt
def create_app(request):
    if request.method == 'POST':
        if not request.user:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        data = json.loads(request.body)
        app_name = data.get('name')
        app_size = data.get('size')
        app_state = 'Pending'

        if type(app_name) != str or len(app_name) > 128:
            return JsonResponse({'error': 'Name length exceeded'}, status=400)

        if app_size is None or not isinstance(app_size, int) or app_size <= 0 or app_size > 2000:
            return JsonResponse({'error': 'Invalid size input'}, status=400)

        if data.get('id') is not None:
            return JsonResponse({'error': 'Id field is not required'}, status=400)

        if data.get('creation_time') is not None:
            return JsonResponse({'error': 'Creation Time field is not required'}, status=400)

        app = App.objects.create(
            user=request.user,
            name=app_name,
            size=app_size,
            state=app_state
        )
        try:
            app.save()
        except Exception as e:
            print(e.messages)

        setup_app(app_name, app_size)
        response_data = {
            'id': app.id,
            'name': app.name,
            'size': app.size,
            'state': app.state,
            'creation_time': app.creation_time
        }
        return JsonResponse(response_data, status=201)


@csrf_exempt
def list_apps(request):
    if request.method == 'GET':
        if not request.user:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        apps = App.objects.filter(user=request.user)
        results = []
        for app in apps:
            pod_list = get_app(app)
            if pod_list.items:
                pod_status = pod_list.items[0].status.phase
                app.state = pod_status 
                app.save()

            results.append({
                'id': app.id,
                'name': app.name,
                'size': app.size,
                'state': app.state,
                'creation_time': app.creation_time
            }) 
        return JsonResponse({'results': results}, status=200)


@csrf_exempt
def separator(request, app_id):
    if request.method == 'GET':
        if not request.user:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        try:
            app = App.objects.get(pk=app_id, user=request.user)
            pod_list = get_app(app)

            if pod_list.items:
                pod_status = pod_list.items[0].status.phase
                app.state = pod_status
                app.save()

            response_data = {
                'id': app.id,
                'name': app.name,
                'size': app.size,
                'state': app.state,
                'creation_time': app.creation_time
            }
            return JsonResponse(response_data, status=200)
        except App.DoesNotExist:
            return JsonResponse({'error': 'App not found'}, status=404)

    elif request.method == 'PUT':
        if not request.user:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        try:
            app = App.objects.get(pk=app_id, user=request.user)
            data = json.loads(request.body)
            if 'size' in data:
                new_size = data.get('size')
                if new_size is None or type(new_size) != int or new_size <= 0 or new_size > 2000:
                    return JsonResponse({'error': 'Invalid size input'}, status=400)

                if new_size <= app.size:
                    return JsonResponse({'error': 'New size must be larger than current size'}, status=400)        

                update_app(app, new_size)
                app.size = new_size
                app.save()
                response_data = {
                    'id': app.id,
                    'name': app.name,
                    'size': app.size,
                    'state': app.state,
                    'creation_time': app.creation_time
                }
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({'error': 'Size field is required'}, status=400)
        except App.DoesNotExist:
            return JsonResponse({'error': 'App not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        if not request.user:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        try:
            app = App.objects.get(pk=app_id, user=request.user)
        except App.DoesNotExist:
            return JsonResponse({'error': 'App not found'}, status=404)

        delete_app(app)
        app.delete()
        return JsonResponse({}, status=204)