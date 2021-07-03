from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ProductCreateForm, ProductVoucherForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Product, Indent


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.dept = form.cleaned_data.get('dept')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('voucher')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "login.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


def category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        cat = Category(category_name=category_name)
        cat.save()
        return redirect('product')
    return render(request, 'category.html', {'msg': 'Product added Successfully!'})


def product_create(request):
    form = ProductCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'data': form,
    }
    return render(request, 'product_create.html', context)


def ProductVoucher(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_data = Indent.objects.filter(id__icontains=q)
    else:
        all_data = Indent.objects.all()

    paginator = Paginator(all_data, 15)  # Show 15 contacts per page.
    page_number = request.GET.get('page')
    total_data = paginator.get_page(page_number)

    form = ProductVoucherForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'data': form,  # 'all': all_data,
        'all_data': total_data
    }
    return render(request, 'product_voucher.html', context)


def updateVoucher(request, id, false=None):
    indent = get_object_or_404(Indent, pk=id)
    form = ProductVoucherForm(request.POST or None, instance=indent)

    if form.is_valid():
        indent = form.save(commit=false)
        indent.save()
        return redirect('voucher')
    else:
        context = {
            'form': form
        }
    return render(request, 'update_voucher.html', context)


def deleteVoucher(request, id):
    data = Indent.objects.get(id=id)
    data.delete()
    return redirect('voucher')
