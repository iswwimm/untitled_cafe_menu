import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from functools import wraps
from menu.models import Coffee, Toast, Sweet
from .forms import CoffeeForm, ToastForm, SweetForm

CATEGORY_MODELS = {
    'coffee': (Coffee, CoffeeForm),
    'toast': (Toast, ToastForm),
    'sweet': (Sweet, SweetForm),
}

COFFEE_GROUPS = [
    {'key': 'basic', 'name': 'Basic Drinks'},
    {'key': 'alternative', 'name': 'Alternative'},
    {'key': 'other', 'name': 'Other Drinks'},
    {'key': 'addon', 'name': 'Add-ons'},
]


def staff_only(view_func):
    """Декоратор для перевірки доступу до staff сторінок"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_staff_authenticated', False):
            return redirect('modifiers:enter_password')
        return view_func(request, *args, **kwargs)
    return wrapper


def enter_password(request):
    """View для введення пароля доступу"""
    if request.session.get('is_staff_authenticated', False):
        return redirect('/modifiers/')

    error_message = None
    correct_password = os.getenv("STAFF_PAGE_PASSWORD") or os.getenv("RENDER")

    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password and password == correct_password:
            request.session['is_staff_authenticated'] = True
            messages.success(request, 'Access granted!')
            return redirect('/modifiers/')
        else:
            error_message = 'Incorrect password. Please try again.'

    context = {'error_message': error_message}
    return render(request, 'modifiers/enter_password.html', context)


def staff_logout(request):
    """View для виходу зі staff режиму"""
    request.session.pop('is_staff_authenticated', None)
    messages.info(request, 'You have been logged out.')
    return redirect('modifiers:enter_password')


def dashboard(request):
    """Dashboard view з перевіркою доступу"""
    if not request.session.get('is_staff_authenticated', False):
        return redirect('modifiers:enter_password')
    
    sections = []
    for key, (model, form_class) in CATEGORY_MODELS.items():
        items = model.objects.filter(is_active=True).order_by('order', 'name')
        section = {
            'name': key,
            'items': items,
        }

        if key == 'coffee':
            # Групування кави
            groups = sorted(set(item.group for item in items))
            grouped_items = []
            for g in groups:
                group_items = items.filter(group=g).order_by('order', 'name')
                grouped_items.append((g, group_items))
            section['grouped_items'] = grouped_items
        sections.append(section)

    return render(request, 'modifiers/dashboard.html', {'sections': sections})



@staff_only
def archive(request):
    coffee_items = Coffee.objects.filter(is_active=False).order_by('group', 'name')
    coffee_groups = ['basic', 'alternative', 'other', 'addon']
    grouped_coffee = {g: [] for g in coffee_groups}
    for item in coffee_items:
        grouped_coffee[item.group].append(item)

    sections = [
        {'name': 'coffee', 'grouped_items': grouped_coffee},
        {'name': 'toast', 'items': Toast.objects.filter(is_active=False)},
        {'name': 'sweet', 'items': Sweet.objects.filter(is_active=False)},
    ]
    return render(request, 'modifiers/archive.html', {'sections': sections})


@staff_only
def add_item(request, category):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, form_class = pair

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # Handle allergens for toast and sweet
            if category in ['toast', 'sweet'] and 'allergens' in form.cleaned_data:
                allergens_list = form.cleaned_data['allergens']
                instance.allergens = ', '.join(allergens_list) if allergens_list else ''
            instance.save()
            return redirect('modifiers:dashboard')
    else:
        form = form_class()

    return render(
        request, 
        'modifiers/item_form.html', 
        {'form': form, 'title': f'Add {category.capitalize()}'}
    )


@staff_only
def edit_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, form_class = pair
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            # Handle allergens for toast and sweet
            if category in ['toast', 'sweet'] and 'allergens' in form.cleaned_data:
                allergens_list = form.cleaned_data['allergens']
                instance.allergens = ', '.join(allergens_list) if allergens_list else ''
            instance.save()
            return redirect('modifiers:dashboard')
    else:
        form = form_class(instance=instance)
        # Pre-populate allergens for toast and sweet
        if category in ['toast', 'sweet'] and instance.allergens:
            allergens_list = [a.strip() for a in instance.allergens.split(',') if a.strip()]
            form.fields['allergens'].initial = allergens_list

    return render(
        request, 
        'modifiers/item_form.html', 
        {'form': form, 'title': f'Edit {category.capitalize()}'}
    )


@staff_only
def delete_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, _ = pair
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        instance.delete()
        return redirect('modifiers:dashboard')

    return render(
        request, 
        'modifiers/item_confirm_delete.html', 
        {'object': instance, 'title': f'Delete {category.capitalize()}'}
    )


@staff_only
def archive_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, _ = pair
    instance = get_object_or_404(model, pk=pk)
    instance.is_active = False
    instance.save()
    return redirect('modifiers:dashboard')


@staff_only
def restore_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:archive')
    model, _ = pair
    instance = get_object_or_404(model, pk=pk)
    instance.is_active = True
    instance.save()
    return redirect('modifiers:archive')
