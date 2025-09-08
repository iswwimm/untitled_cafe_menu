# modifiers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from menu.models import Coffee, Toast, Sweet
from .forms import CoffeeForm, ToastForm, SweetForm

def staff_check(user):
    return user.is_staff

@login_required
@user_passes_test(staff_check)
def dashboard(request):
    coffees = Coffee.objects.all()
    toasts = Toast.objects.all()
    sweets = Sweet.objects.all()
    return render(request, 'modifiers/dashboard.html', {
        'coffees': coffees,
        'toasts': toasts,
        'sweets': sweets
    })

@login_required
@user_passes_test(staff_check)
def add_item(request, category):
    if category == 'coffee':
        form_class = CoffeeForm
    elif category == 'toast':
        form_class = ToastForm
    elif category == 'sweet':
        form_class = SweetForm
    else:
        return redirect('modifiers:dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = form_class()

    return render(request, 'modifiers/item_form.html', {'form': form, 'category': category})

@login_required
@user_passes_test(staff_check)
def edit_item(request, category, pk):
    if category == 'coffee':
        item = get_object_or_404(Coffee, pk=pk)
        form_class = CoffeeForm
    elif category == 'toast':
        item = get_object_or_404(Toast, pk=pk)
        form_class = ToastForm
    elif category == 'sweet':
        item = get_object_or_404(Sweet, pk=pk)
        form_class = SweetForm
    else:
        return redirect('modifiers:dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = form_class(instance=item)

    return render(request, 'modifiers/item_form.html', {'form': form, 'category': category, 'item': item})

@login_required
@user_passes_test(staff_check)
def delete_item(request, category, pk):
    if category == 'coffee':
        item = get_object_or_404(Coffee, pk=pk)
    elif category == 'toast':
        item = get_object_or_404(Toast, pk=pk)
    elif category == 'sweet':
        item = get_object_or_404(Sweet, pk=pk)
    else:
        return redirect('modifiers:dashboard')

    if request.method == 'POST':
        item.delete()
        return redirect('modifiers:dashboard')

    return render(request, 'modifiers/confirm_delete.html', {'item': item, 'category': category})
