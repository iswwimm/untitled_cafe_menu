from django.shortcuts import render, get_object_or_404, redirect
from menu.models import Coffee, Toast, Sweet
from .forms import CoffeeForm, ToastForm, SweetForm

# ---------------- Dashboard ----------------
def dashboard(request):
    sections = [
        {'category': 'coffee', 'items': Coffee.objects.all()},
        {'category': 'toast', 'items': Toast.objects.all()},
        {'category': 'sweet', 'items': Sweet.objects.all()},
    ]
    return render(request, 'modifiers/dashboard.html', {'sections': sections})


# ---------------- Coffee CRUD ----------------
def add_coffee(request):
    if request.method == 'POST':
        form = CoffeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = CoffeeForm()
    return render(request, 'modifiers/item_form.html', {'form': form, 'title': 'Add Coffee'})

def edit_coffee(request, pk):
    coffee = get_object_or_404(Coffee, pk=pk)
    if request.method == 'POST':
        form = CoffeeForm(request.POST, instance=coffee)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = CoffeeForm(instance=coffee)
    return render(request, 'modifiers/item_form.html', {'form': form, 'title': 'Edit Coffee'})

def delete_coffee(request, pk):
    coffee = get_object_or_404(Coffee, pk=pk)
    if request.method == 'POST':
        coffee.delete()
        return redirect('modifiers:dashboard')
    return render(request, 'modifiers/item_confirm_delete.html', {'object': coffee, 'title': 'Delete Coffee'})

# ---------------- Toast CRUD ----------------
def add_toast(request):
    if request.method == 'POST':
        form = ToastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = ToastForm()
    return render(request, 'modifiers/item_form.html', {'form': form, 'title': 'Add Toast'})

def edit_toast(request, pk):
    toast = get_object_or_404(Toast, pk=pk)
    if request.method == 'POST':
        form = ToastForm(request.POST, request.FILES, instance=toast)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = ToastForm(instance=toast)
    return render(request, 'modifiers/item_form.html', {'form': form, 'title': 'Edit Toast'})

def delete_toast(request, pk):
    toast = get_object_or_404(Toast, pk=pk)
    if request.method == 'POST':
        toast.delete()
        return redirect('modifiers:dashboard')
    return render(request, 'modifiers/item_confirm_delete.html', {'object': toast, 'title': 'Delete Toast'})

# ---------------- Sweet CRUD ----------------
def add_sweet(request):
    if request.method == 'POST':
        form = SweetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = SweetForm()
    return render(request, 'modifiers/item_form.html', {'form': form, 'title': 'Add Sweet'})

def edit_sweet(request, pk):
    sweet = get_object_or_404(Sweet, pk=pk)
    if request.method == 'POST':
        form = SweetForm(request.POST, request.FILES, instance=sweet)
        if form.is_valid():
            form.save()
            return redirect('modifiers:dashboard')
    else:
        form = SweetForm(instance=sweet)
    return render(request, 'modifiers/item_form.html', {'form': form, 'title': 'Edit Sweet'})

def delete_sweet(request, pk):
    sweet = get_object_or_404(Sweet, pk=pk)
    if request.method == 'POST':
        sweet.delete()
        return redirect('modifiers:dashboard')
    return render(request, 'modifiers/item_confirm_delete.html', {'object': sweet, 'title': 'Delete Sweet'})
