from django.shortcuts import render, get_object_or_404, redirect
from menu.models import Coffee, Toast, Sweet
from .forms import CoffeeForm, ToastForm, SweetForm

CATEGORY_MODELS = {
    'coffee': (Coffee, CoffeeForm),
    'toast': (Toast, ToastForm),
    'sweet': (Sweet, SweetForm),
}


def dashboard(request):
    # показуємо тільки активні позиції на dashboard
    sections = [
        {'name': 'coffee', 'items': Coffee.objects.filter(is_active=True)},
        {'name': 'toast', 'items': Toast.objects.filter(is_active=True)},
        {'name': 'sweet', 'items': Sweet.objects.filter(is_active=True)},
    ]
    return render(request, 'modifiers/dashboard.html', {'sections': sections})


def archive(request):
    sections = [
        {'name': 'coffee', 'items': Coffee.objects.filter(is_active=False)},
        {'name': 'toast', 'items': Toast.objects.filter(is_active=False)},
        {'name': 'sweet', 'items': Sweet.objects.filter(is_active=False)},
    ]
    return render(request, 'modifiers/archive.html', {'sections': sections})


def add_item(request, category):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, form_class = pair

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = form_class()

    return render(request, 'modifiers/item_form.html', {'form': form, 'title': f'Add {category.capitalize()}'})


def edit_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, form_class = pair
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = form_class(instance=instance)

    return render(request, 'modifiers/item_form.html', {'form': form, 'title': f'Edit {category.capitalize()}'})


def delete_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, _ = pair
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        instance.delete()
        return redirect('modifiers:dashboard')

    return render(request, 'modifiers/item_confirm_delete.html', {'object': instance, 'title': f'Delete {category.capitalize()}'})


def archive_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:dashboard')
    model, _ = pair
    instance = get_object_or_404(model, pk=pk)
    instance.is_active = False
    instance.save()
    return redirect('modifiers:dashboard')


def restore_item(request, category, pk):
    pair = CATEGORY_MODELS.get(category)
    if not pair:
        return redirect('modifiers:archive')
    model, _ = pair
    instance = get_object_or_404(model, pk=pk)
    instance.is_active = True
    instance.save()
    return redirect('modifiers:archive')
