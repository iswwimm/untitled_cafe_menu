from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Coffee, Toast, Sweet

def home(request):
    return render(request, 'menu/home.html')

def coffee_list(request):
    coffees = Coffee.objects.filter(is_active=True).order_by('group', 'order', 'name')

    groups = [
        {'key': 'basic', 'name': 'Basic Drinks', 'class': 'base_coffee', 'items': coffees.filter(group='basic').order_by('order', 'name')},
        {'key': 'alternative', 'name': 'Alternative', 'class': 'alternative_coffee', 'items': coffees.filter(group='alternative').order_by('order', 'name')},
        {'key': 'other', 'name': 'Other Drinks', 'class': 'other_drink', 'items': coffees.filter(group='other').order_by('order', 'name')},
        {'key': 'addon', 'name': 'Add-ons', 'class': 'addon', 'items': coffees.filter(group='addon').order_by('order', 'name')},
    ]

    return render(request, 'menu/coffee.html', {'groups': groups})

def toasts_list(request):
    toasts = Toast.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'menu/toasts.html', {'toasts': toasts})

def sweets_list(request):
    sweets = Sweet.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'menu/sweets.html', {'sweets': sweets})

@csrf_exempt
@require_http_methods(["POST"])
def update_order(request, model_type):
    """AJAX endpoint для оновлення порядку елементів"""
    print(f"Received request for model_type: {model_type}")
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        group = data.get('group', None)
        
        print(f"Items to update: {items}")
        print(f"Group: {group}")
        
        if model_type == 'coffee':
            model_class = Coffee
        elif model_type == 'toast':
            model_class = Toast
        elif model_type == 'sweet':
            model_class = Sweet
        else:
            print(f"Invalid model type: {model_type}")
            return JsonResponse({'error': 'Invalid model type'}, status=400)
        
        # Оновлюємо порядок для кожного елемента
        for index, item_id in enumerate(items):
            try:
                item = model_class.objects.get(id=item_id)
                # Для кави перевіряємо, що елемент належить до правильної групи
                if model_type == 'coffee' and group and item.group != group:
                    print(f"Skipping item {item_id} - wrong group")
                    continue
                item.order = index
                item.save()
                print(f"Updated item {item_id} to order {index}")
            except model_class.DoesNotExist:
                print(f"Item {item_id} not found")
                continue
        
        print("Order update completed successfully")
        return JsonResponse({'success': True})
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"General error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
